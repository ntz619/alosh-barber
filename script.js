const header = document.querySelector('.site-header');
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const root = document.documentElement;

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;


    // centered-anchor-navigation
    function getNaturalAnchorMetrics(target) {
      root.classList.add('scroll-measure');
      void document.body.offsetHeight;

      let focus = target;
      if (target.classList.contains('stack-panel')) focus = target.querySelector('.panel-inner') || target;
      if (target.id === 'visit') focus = target.querySelector('.visit-card') || target;

      const rect = focus.getBoundingClientRect();
      const metrics = { top: rect.top + window.scrollY, height: rect.height };

      root.classList.remove('scroll-measure');
      void document.body.offsetHeight;
      return metrics;
    }

    function scrollTargetToCenter(target, updateHash = true) {
      if (!target) return;
      if (target.id === 'top') {
        window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
        if (updateHash) history.replaceState(null, '', '#top');
        return;
      }

      const { top, height } = getNaturalAnchorMetrics(target);
      const headerHeight = header?.offsetHeight || 0;
      const safeTop = headerHeight + 12;
      const safeBottom = 18;
      const availableHeight = Math.max(window.innerHeight - safeTop - safeBottom, 1);
      const visibleHeight = Math.min(height, availableHeight);
      const centeredTop = top - safeTop - Math.max((availableHeight - visibleHeight) / 2, 0);
      const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
      const destination = clamp(centeredTop, 0, maxScroll);

      window.scrollTo({ top: destination, behavior: reducedMotion ? 'auto' : 'smooth' });
      if (updateHash && target.id) history.replaceState(null, '', `#${target.id}`);
    }

    document.querySelectorAll('a[href^="#"]').forEach(link => {
      link.addEventListener('click', event => {
        const hash = link.getAttribute('href');
        if (!hash || hash === '#') return;
        const target = document.querySelector(hash);
        if (!target) return;
        event.preventDefault();

        document.body.classList.remove('menu-open');
        menuToggle?.setAttribute('aria-expanded', 'false');
        mobileMenu?.setAttribute('aria-hidden', 'true');

        // Call directly instead of deferring through requestAnimationFrame. This
        // makes repeated quick-link use reliable even during/after long scrolling.
        scrollTargetToCenter(target);
      });
    });

    window.addEventListener('load', () => {
      if (!window.location.hash) return;
      const target = document.querySelector(window.location.hash);
      if (target) setTimeout(() => scrollTargetToCenter(target, false), 0);
    }, { once: true });

    function updateShopStatus() {
      // Verified Rostock hours: Mon–Fri 08:30–19:00, Sat 08:30–16:00, Sun closed.
      // Europe/Berlin handles German daylight-saving time automatically.
      const schedule = {
        0: null,
        1: [8 * 60 + 30, 19 * 60],
        2: [8 * 60 + 30, 19 * 60],
        3: [8 * 60 + 30, 19 * 60],
        4: [8 * 60 + 30, 19 * 60],
        5: [8 * 60 + 30, 19 * 60],
        6: [8 * 60 + 30, 16 * 60]
      };
      const weekdayMap = { Sun:0, Mon:1, Tue:2, Wed:3, Thu:4, Fri:5, Sat:6 };
      const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
      const parts = new Intl.DateTimeFormat('en-GB', {
        timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
      }).formatToParts(new Date());
      const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
      const day = weekdayMap[values.weekday];
      const nowMinutes = Number(values.hour) * 60 + Number(values.minute);
      const hours = schedule[day];
      const formatTime = minutes => `${String(Math.floor(minutes / 60)).padStart(2,'0')}:${String(minutes % 60).padStart(2,'0')}`;

      let status = 'Closed now';
      let detail = '';

      if (hours && nowMinutes >= hours[0] && nowMinutes < hours[1]) {
        status = 'Open now';
        detail = `Until ${formatTime(hours[1])}`;
      } else if (hours && nowMinutes < hours[0]) {
        status = 'Opens today';
        detail = formatTime(hours[0]);
      } else {
        for (let offset = 1; offset <= 7; offset++) {
          const nextDay = (day + offset) % 7;
          const nextHours = schedule[nextDay];
          if (!nextHours) continue;
          status = day === 0 ? 'Closed today' : 'Closed now';
          detail = `Opens ${offset === 1 ? 'tomorrow' : dayNames[nextDay]} ${formatTime(nextHours[0])}`;
          break;
        }
      }

      document.querySelectorAll('[data-shop-status]').forEach(el => { el.textContent = status; });
      document.querySelectorAll('[data-shop-detail]').forEach(el => { el.textContent = detail; });
    }

    updateShopStatus();
    setInterval(updateShopStatus, 60000);

    function handleScrollState(){
      header.classList.toggle('scrolled', window.scrollY > 18);

      document.querySelectorAll('.parallax').forEach(el => {
        if (reducedMotion) return;
        const speed = parseFloat(el.dataset.speed || '0.12');
        const host = el.closest('.hero, .panel-copy, .cuts-stage') || el.parentElement;
        const rect = host.getBoundingClientRect();
        const move = (window.innerHeight - rect.top) * speed;
        el.style.transform = `translate3d(0, ${-move}px, 0)`;
      });

      const stickyPanels = [...document.querySelectorAll('.stack-panel')];
      const topOffset = parseFloat(getComputedStyle(root).getPropertyValue('--header')) + 12;
      stickyPanels.forEach((panel, index) => {
        const inner = panel.querySelector('.panel-inner');
        const next = stickyPanels[index + 1];
        if (!next || reducedMotion) {
          inner.style.transform = '';
          inner.style.filter = '';
          return;
        }
        const distance = next.getBoundingClientRect().top - topOffset;
        const progress = clamp((180 - distance) / 180, 0, 1);
        inner.style.transform = `scale(${1 - progress * .025}) translateY(${-progress * 6}px)`;
        inner.style.filter = `brightness(${1 - progress * .14})`;
      });
    }

    window.addEventListener('scroll', () => requestAnimationFrame(handleScrollState), { passive: true });
    window.addEventListener('resize', handleScrollState);

    menuToggle?.addEventListener('click', () => {
      const open = document.body.classList.toggle('menu-open');
      menuToggle.setAttribute('aria-expanded', String(open));
      mobileMenu.setAttribute('aria-hidden', String(!open));
    });

    document.querySelectorAll('.mobile-menu a').forEach(link => {
      link.addEventListener('click', () => {
        document.body.classList.remove('menu-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
      });
    });

    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14 });

    document.querySelectorAll('.reveal, .animate-on-scroll').forEach(el => revealObserver.observe(el));


    // cuts-horizontal-carousel-v3
    function setupCutsCarousel() {
      const track = document.querySelector('[data-cuts-carousel]');
      if (!track) return;

      const originals = [...track.children];
      if (!originals.length) return;

      originals.forEach(card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        clone.classList.add('in-view');
        clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
        track.appendChild(clone);
      });

      const originalCount = originals.length;
      const AUTO_DELAY = 3200;
      const RESUME_DELAY = 3600;
      const SCROLL_DURATION = 750;

      let autoTimer = null;
      let settleTimer = null;
      let isDragging = false;
      let dragStartX = 0;
      let dragStartScrollLeft = 0;
      let loopWidth = 0;

      const cards = () => [...track.children];

      const updateLoopWidth = () => {
        const firstClone = track.children[originalCount];
        loopWidth = firstClone ? firstClone.offsetLeft - track.children[0].offsetLeft : track.scrollWidth / 2;
      };

      const centeredLeft = card => {
        const raw = card.offsetLeft - (track.clientWidth - card.offsetWidth) / 2;
        return Math.max(0, raw);
      };

      const normalizeLoopPosition = () => {
        if (!loopWidth) return;
        while (track.scrollLeft >= loopWidth) track.scrollLeft -= loopWidth;
        while (track.scrollLeft < 0) track.scrollLeft += loopWidth;
      };

      const nearestCardIndex = () => {
        const center = track.scrollLeft + track.clientWidth / 2;
        const list = cards();
        let nearest = 0;
        let distance = Infinity;
        list.forEach((card, index) => {
          const cardCenter = card.offsetLeft + card.offsetWidth / 2;
          const d = Math.abs(cardCenter - center);
          if (d < distance) {
            distance = d;
            nearest = index;
          }
        });
        return nearest;
      };

      const clearAuto = () => {
        if (autoTimer) clearTimeout(autoTimer);
        autoTimer = null;
      };

      const scheduleAuto = (delay = AUTO_DELAY) => {
        clearAuto();
        if (reducedMotion) return;
        autoTimer = setTimeout(advance, delay);
      };

      const pauseForInteraction = (delay = RESUME_DELAY) => {
        clearAuto();
        if (settleTimer) clearTimeout(settleTimer);
        settleTimer = setTimeout(() => {
          normalizeLoopPosition();
          scheduleAuto(500);
        }, delay);
      };

      function advance() {
        if (isDragging || document.visibilityState !== 'visible') {
          scheduleAuto(900);
          return;
        }

        normalizeLoopPosition();
        let current = nearestCardIndex();
        if (current >= originalCount) current -= originalCount;

        // Move to the next original; after the final original we animate to the
        // identical first clone, then invisibly jump back to the real first card.
        const targetIndex = current === originalCount - 1 ? originalCount : current + 1;
        const target = track.children[targetIndex];
        if (!target) {
          scheduleAuto();
          return;
        }

        track.scrollTo({
          left: centeredLeft(target),
          behavior: 'smooth'
        });

        clearTimeout(settleTimer);
        settleTimer = setTimeout(() => {
          if (targetIndex === originalCount) {
            const first = track.children[0];
            track.scrollLeft = centeredLeft(first);
          }
          scheduleAuto();
        }, SCROLL_DURATION);
      }

      // Native swipe/trackpad/manual scrolling always wins. Autoplay resumes from
      // the visitor's new position instead of resetting to the first image.
      track.addEventListener('touchstart', () => pauseForInteraction(), { passive: true });
      track.addEventListener('touchend', () => pauseForInteraction(), { passive: true });
      track.addEventListener('wheel', () => pauseForInteraction(2800), { passive: true });
      track.addEventListener('focusin', () => pauseForInteraction(), { passive: true });

      track.addEventListener('keydown', event => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        pauseForInteraction();
        const list = cards();
        let current = nearestCardIndex();
        if (current >= originalCount) current -= originalCount;
        const direction = event.key === 'ArrowRight' ? 1 : -1;
        const targetIndex = (current + direction + originalCount) % originalCount;
        track.scrollTo({ left: centeredLeft(list[targetIndex]), behavior: reducedMotion ? 'auto' : 'smooth' });
      });

      track.addEventListener('pointerdown', event => {
        if (event.pointerType !== 'mouse' || event.button !== 0) return;
        clearAuto();
        if (settleTimer) clearTimeout(settleTimer);
        isDragging = true;
        dragStartX = event.clientX;
        dragStartScrollLeft = track.scrollLeft;
        track.classList.add('is-dragging');
        track.setPointerCapture?.(event.pointerId);
      });

      track.addEventListener('pointermove', event => {
        if (!isDragging) return;
        track.scrollLeft = dragStartScrollLeft - (event.clientX - dragStartX);
      });

      const stopDragging = event => {
        if (!isDragging) return;
        isDragging = false;
        track.classList.remove('is-dragging');
        if (event?.pointerId != null && track.hasPointerCapture?.(event.pointerId)) {
          track.releasePointerCapture(event.pointerId);
        }
        pauseForInteraction();
      };

      track.addEventListener('pointerup', stopDragging);
      track.addEventListener('pointercancel', stopDragging);
      track.addEventListener('lostpointercapture', stopDragging);

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') scheduleAuto(900);
        else clearAuto();
      });

      window.addEventListener('resize', () => {
        updateLoopWidth();
        normalizeLoopPosition();
      });

      requestAnimationFrame(() => {
        updateLoopWidth();
        scheduleAuto(1200);
      });
    }

    setupCutsCarousel();

    function createCarousel({ trackSelector, itemSelector, prevSelector, nextSelector, progressSelector, mode = 'offset', autoplay = 0 }) {
      const track = document.querySelector(trackSelector);
      const items = [...document.querySelectorAll(itemSelector)];
      const prev = document.querySelector(prevSelector);
      const next = document.querySelector(nextSelector);
      const progress = progressSelector ? document.querySelector(progressSelector) : null;
      if (!track || !items.length) return;

      let index = 0;
      let timer;
      let touchStartX = 0;

      function update() {
        items.forEach((item, itemIndex) => item.classList.toggle('active', itemIndex === index));
        if (mode === 'offset') {
          track.style.transform = `translateX(${-items[index].offsetLeft}px)`;
        } else {
          track.style.transform = `translateX(-${index * 100}%)`;
        }
        if (progress) {
          progress.style.transform = `translateX(${index * 100}%)`;
        }
      }

      function restart() {
        if (!autoplay) return;
        clearInterval(timer);
        timer = setInterval(goNext, autoplay);
      }

      function goNext() {
        index = (index + 1) % items.length;
        update();
        restart();
      }

      function goPrev() {
        index = (index - 1 + items.length) % items.length;
        update();
        restart();
      }

      prev?.addEventListener('click', goPrev);
      next?.addEventListener('click', goNext);

      track.addEventListener('touchstart', e => {
        touchStartX = e.touches[0].clientX;
      }, { passive: true });

      track.addEventListener('touchend', e => {
        const diff = e.changedTouches[0].clientX - touchStartX;
        if (Math.abs(diff) > 40) {
          diff < 0 ? goNext() : goPrev();
        }
      }, { passive: true });

      window.addEventListener('resize', update);
      update();
      restart();
    }

    createCarousel({
      trackSelector: '.gallery-track',
      itemSelector: '.gallery-card',
      prevSelector: '[data-gallery-prev]',
      nextSelector: '[data-gallery-next]',
      mode: 'offset'
    });

    createCarousel({
      trackSelector: '.review-track',
      itemSelector: '.review-card',
      prevSelector: '[data-review-prev]',
      nextSelector: '[data-review-next]',
      progressSelector: '.review-progress span',
      autoplay: 6500,
      mode: 'percent'
    });

    document.getElementById('year').textContent = new Date().getFullYear();
    handleScrollState();
