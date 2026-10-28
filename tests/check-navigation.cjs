const fs = require('fs'), vm = require('vm'), assert = require('assert/strict');
class Element {
  constructor() { this.listeners = {}; this.attrs = {}; this.classes = new Set(); this.classList = {
    add: name => this.classes.add(name), remove: name => this.classes.delete(name),
    contains: name => this.classes.has(name), toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name)
  }; }
  addEventListener(name, callback) { this.listeners[name] = callback; }
  setAttribute(name, value) { this.attrs[name] = value; }
  focus() { focused = this; }
  contains(target) { return this === target || (this.children || []).some(child => child.contains(target)); }
  fire(name, event = {}) { this.listeners[name]?.(event); }
}
let focused;
const header = new Element(), nav = new Element();
const groups = [0, 1].map(() => {
  const group = new Element(), button = new Element(), link = new Element();
  group.children = [button, link]; group.querySelector = selector => selector === 'button' ? button : link;
  return group;
});
nav.querySelectorAll = () => groups; nav.children = groups; nav.closest = () => header;
let toggle, viewportChange;
nav.before = button => { toggle = button; header.children = [toggle, nav]; };
const document = new Element();
document.querySelectorAll = () => [nav]; document.createElement = () => new Element();
vm.runInNewContext(fs.readFileSync('dist/navigation.js', 'utf8'), {
  document, matchMedia: () => ({addEventListener: (_, fn) => {viewportChange = fn;}})
});
const first = groups[0], second = groups[1], button = first.querySelector('button');
toggle.fire('click'); assert.equal(toggle.attrs['aria-expanded'], 'true');
button.fire('click'); assert.equal(button.attrs['aria-expanded'], 'true');
button.fire('click'); assert.equal(button.attrs['aria-expanded'], 'false');
first.fire('keydown', {key: 'ArrowDown', target: button, preventDefault() {}});
assert.equal(focused, first.querySelector('a'));
first.fire('keydown', {key: 'Escape', stopPropagation() {}});
assert.equal(focused, button); assert.equal(button.attrs['aria-expanded'], 'false');
header.fire('keydown', {key: 'Escape'});
assert.equal(toggle.attrs['aria-expanded'], 'false'); assert.equal(focused, toggle);
toggle.fire('click'); button.fire('click'); second.querySelector('button').fire('click');
assert.equal(button.attrs['aria-expanded'], 'false');
assert.equal(second.querySelector('button').attrs['aria-expanded'], 'true');
document.fire('pointerdown', {target: new Element()});
assert.equal(toggle.attrs['aria-expanded'], 'false');
toggle.fire('click'); header.fire('focusout', {relatedTarget: new Element()});
assert.equal(toggle.attrs['aria-expanded'], 'false');
toggle.fire('click'); viewportChange(); assert.equal(toggle.attrs['aria-expanded'], 'false');
console.log('Navigation toggling, exclusivity, keyboard focus, dismissal and breakpoint reset pass');
