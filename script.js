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

    // cuts-horizontal-carousel-v5
    function setupCutsCarousel() {
      const track = document.querySelector('[data-cuts-carousel]');
      if (!track) return;

      const originals = [...track.children];
      if (!originals.length) return;

      const cloneCard = card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        clone.classList.add('in-view');
        clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
        return clone;
      };

      // One full copy on each side gives us a repeating visual strip:
      // [copy] [real cards] [copy]. We always recycle the scroll coordinate only
      // after motion has fully stopped, while the visible pixels are identical.
      const left = document.createDocumentFragment();
      originals.forEach(card => left.appendChild(cloneCard(card)));
      track.prepend(left);

      const right = document.createDocumentFragment();
      originals.forEach(card => right.appendChild(cloneCard(card)));
      track.append(right);

      const count = originals.length;
      const middleStart = count;
      const middleEnd = middleStart + count - 1;
      const AUTO_DELAY = 3200;
      const RESUME_DELAY = 3600;
      const AUTO_DURATION = 720;

      let period = 0;
      let autoTimer = null;
      let manualTimer = null;
      let animationFrame = null;
      let dragging = false;
      let dragStartX = 0;
      let dragStartScrollLeft = 0;
      let programmaticUntil = 0;

      const allCards = () => [...track.children];
      const centeredLeft = card => card.offsetLeft + card.offsetWidth / 2 - track.clientWidth / 2;

      const updatePeriod = () => {
        const leftFirst = track.children[0];
        const middleFirst = track.children[middleStart];
        if (leftFirst && middleFirst) period = middleFirst.offsetLeft - leftFirst.offsetLeft;
      };

      const nearestIndex = () => {
        const viewportCenter = track.scrollLeft + track.clientWidth / 2;
        let nearest = middleStart;
        let best = Infinity;

        allCards().forEach((card, index) => {
          const distance = Math.abs((card.offsetLeft + card.offsetWidth / 2) - viewportCenter);
          if (distance < best) {
            best = distance;
            nearest = index;
          }
        });

        return nearest;
      };

      const markProgrammatic = (ms = 140) => {
        programmaticUntil = performance.now() + ms;
      };

      const jumpBy = amount => {
        if (!amount || !period) return;
        markProgrammatic(180);
        track.scrollLeft += amount;
      };

      const normalizeToMiddle = () => {
        updatePeriod();
        let index = nearestIndex();

        if (index < middleStart) {
          jumpBy(period);
          index += count;
        } else if (index > middleEnd) {
          jumpBy(-period);
          index -= count;
        }

        return index;
      };

      const clearAuto = () => {
        if (autoTimer) clearTimeout(autoTimer);
        autoTimer = null;
      };

      const clearManualTimer = () => {
        if (manualTimer) clearTimeout(manualTimer);
        manualTimer = null;
      };

      const cancelAnimation = () => {
        if (animationFrame) cancelAnimationFrame(animationFrame);
        animationFrame = null;
      };

      const animateTo = (targetLeft, duration, onDone) => {
        cancelAnimation();
        const startLeft = track.scrollLeft;
        const distance = targetLeft - startLeft;
        const startTime = performance.now();

        const tick = now => {
          const progress = Math.min((now - startTime) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          markProgrammatic(180);
          track.scrollLeft = startLeft + distance * eased;

          if (progress < 1) {
            animationFrame = requestAnimationFrame(tick);
            return;
          }

          animationFrame = null;
          markProgrammatic(180);
          requestAnimationFrame(() => onDone?.());
        };

        animationFrame = requestAnimationFrame(tick);
      };

      const scheduleAuto = (delay = AUTO_DELAY) => {
        clearAuto();
        if (reducedMotion) return;
        autoTimer = setTimeout(advance, delay);
      };

      const beginManualInteraction = () => {
        clearAuto();
        clearManualTimer();
        cancelAnimation();
      };

      const scheduleResume = (delay = RESUME_DELAY) => {
        clearManualTimer();
        manualTimer = setTimeout(() => {
          normalizeToMiddle();
          scheduleAuto(delay);
        }, 220);
      };

      function advance() {
        if (dragging || document.visibilityState !== 'visible') {
          scheduleAuto(900);
          return;
        }

        const current = normalizeToMiddle();
        const targetIndex = current + 1;
        const target = track.children[targetIndex];

        if (!target) {
          scheduleAuto();
          return;
        }

        animateTo(centeredLeft(target), AUTO_DURATION, () => {
          // When the first right-side clone is centered, recycle the coordinate to
          // the real first card. Because both sets are pixel-identical and there is
          // no browser-controlled smooth scroll or scroll snapping, this is invisible.
          if (targetIndex > middleEnd) jumpBy(-period);
          scheduleAuto();
        });
      }

      track.addEventListener('scroll', () => {
        if (performance.now() < programmaticUntil || dragging || animationFrame) return;
        clearAuto();
        scheduleResume();
      }, { passive: true });

      track.addEventListener('touchstart', beginManualInteraction, { passive: true });
      track.addEventListener('touchend', () => scheduleResume(), { passive: true });
      track.addEventListener('wheel', () => {
        beginManualInteraction();
        scheduleResume(2800);
      }, { passive: true });

      track.addEventListener('keydown', event => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        beginManualInteraction();
        const current = normalizeToMiddle();
        const direction = event.key === 'ArrowRight' ? 1 : -1;
        const target = track.children[current + direction];
        if (!target) return;

        animateTo(centeredLeft(target), 560, () => {
          normalizeToMiddle();
          scheduleAuto(RESUME_DELAY);
        });
      });

      track.addEventListener('pointerdown', event => {
        if (event.pointerType !== 'mouse' || event.button !== 0) return;
        beginManualInteraction();
        dragging = true;
        dragStartX = event.clientX;
        dragStartScrollLeft = track.scrollLeft;
        track.classList.add('is-dragging');
        track.setPointerCapture?.(event.pointerId);
      });

      track.addEventListener('pointermove', event => {
        if (!dragging) return;
        track.scrollLeft = dragStartScrollLeft - (event.clientX - dragStartX);
      });

      const stopDragging = event => {
        if (!dragging) return;
        dragging = false;
        track.classList.remove('is-dragging');
        if (event?.pointerId != null && track.hasPointerCapture?.(event.pointerId)) {
          track.releasePointerCapture(event.pointerId);
        }
        scheduleResume();
      };

      track.addEventListener('pointerup', stopDragging);
      track.addEventListener('pointercancel', stopDragging);
      track.addEventListener('lostpointercapture', stopDragging);

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') scheduleAuto(900);
        else beginManualInteraction();
      });

      window.addEventListener('resize', () => {
        beginManualInteraction();
        requestAnimationFrame(() => {
          updatePeriod();
          const index = normalizeToMiddle();
          const card = track.children[index];
          if (card) {
            markProgrammatic(200);
            track.scrollLeft = centeredLeft(card);
          }
          scheduleAuto(1000);
        });
      });

      // Start on the real first card and center it precisely. Two frames ensure the
      // browser has final card widths before we calculate the initial position.
      requestAnimationFrame(() => requestAnimationFrame(() => {
        updatePeriod();
        const first = track.children[middleStart];
        if (first) {
          markProgrammatic(220);
          track.scrollLeft = centeredLeft(first);
        }
        scheduleAuto(1400);
      }));
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
