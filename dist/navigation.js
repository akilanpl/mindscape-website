// Consistent disclosure controls for keyboard, pointer and touch.
document.querySelectorAll('.glass-nav').forEach((nav, index) => {
  const groups = [...nav.querySelectorAll('.nav-research')];
  const closeMenus = () => groups.forEach(group => {
    group.classList.remove('is-open');
    group.querySelector('button').setAttribute('aria-expanded', 'false');
  });
  groups.forEach(group => {
    const button = group.querySelector('button');
    const set = open => {
      closeMenus();
      group.classList.toggle('is-open', open);
      button.setAttribute('aria-expanded', String(open));
    };
    button.addEventListener('click', () => set(!group.classList.contains('is-open')));
    group.addEventListener('focusout', event => {
      if (!group.contains(event.relatedTarget)) {
        group.classList.remove('is-open');
        button.setAttribute('aria-expanded', 'false');
      }
    });
    group.addEventListener('keydown', event => {
      if (event.key === 'Escape' && group.classList.contains('is-open')) {
        event.stopPropagation(); closeMenus(); button.focus();
      }
      if (event.key === 'ArrowDown' && event.target === button) {
        event.preventDefault(); set(true); group.querySelector('a').focus();
      }
    });
  });
  nav.id ||= `site-navigation-${index}`;
  const toggle = document.createElement('button');
  toggle.type = 'button'; toggle.className = 'mobile-nav-toggle'; toggle.textContent = 'Menu';
  toggle.setAttribute('aria-controls', nav.id); toggle.setAttribute('aria-expanded', 'false');
  nav.before(toggle);
  const header = nav.closest('.floating-header');
  header.classList.add('disclosure-header');
  const setMobile = open => {
    header.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close menu' : 'Menu';
    if (!open) closeMenus();
  };
  toggle.addEventListener('click', () => setMobile(!header.classList.contains('nav-open')));
  header.addEventListener('keydown', event => {
    if (event.key === 'Escape') { setMobile(false); toggle.focus(); }
  });
  header.addEventListener('focusout', event => {
    if (!header.contains(event.relatedTarget)) setMobile(false);
  });
  document.addEventListener('pointerdown', event => {
    if (!header.contains(event.target)) setMobile(false);
    else if (!groups.some(group => group.contains(event.target))) closeMenus();
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) setMobile(false); });
  matchMedia('(max-width: 760px)').addEventListener('change', () => setMobile(false));
});
