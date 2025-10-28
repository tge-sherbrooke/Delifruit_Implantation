document.addEventListener("DOMContentLoaded", () => {
  const selectors = [];

  for (let i = 1; i <= 3; i++) {
    selectors.push(`#section_${i}`);
    selectors.push(`#section_${i} > div`);
    selectors.push(`#section_${i} h2`);
    selectors.push(`#section_${i} p`);
    selectors.push(`#section_${i} article`);
    selectors.push(`#m_section_${i}`);
    selectors.push(`#m_section_${i} > div`);
    selectors.push(`#m_section_${i} h2`);
    selectors.push(`#m_section_${i} p`);
    selectors.push(`#m_section_${i} article`);
  }

  selectors.push(`#a_section_2`);
  selectors.push(`#a_section_2 h2`);
  selectors.push(`#a_section_2 p`);
  selectors.push(`#image_fin_article`);
  selectors.push(`#image_fin_article h2`);
  selectors.push(`#image_fin_article p`);
  selectors.push(`#image_fin_article img`);
  selectors.push(`#image_fin_article aside`);

  // Exemple d'utilisation avec querySelectorAll
  const elements = document.querySelectorAll(selectors.join(","));

  // Tu peux ensuite faire ce que tu veux avec ces éléments
  elements.forEach(el => el.classList.add("fade-in-up"));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      } else {
        entry.target.classList.remove("visible");
      }
    });
  }, { threshold: 0.1 });

  let delay = 0;
  elements.forEach(el => {
    el.style.transitionDelay = `${delay}s`;
    observer.observe(el);
    delay += 0.1;
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll("#section_1 .image_section_1");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;

        // Appliquer animation selon l'ID ou la position
        if (img.id === "left") {
          img.classList.add("animate-x-left");
        } else if (img.id === "right") {
          img.classList.add("animate-x-right");
        }

        img.classList.add("visible");
      } else {
        entry.target.classList.remove("visible", "animate-x-left", "animate-x-right");
      }
    });
  }, { threshold: 0.1 });

  images.forEach(img => {
    observer.observe(img);
  });
});

// Carousel: un cran par clic + caption au clic, hide on mouseleave
document.addEventListener('DOMContentLoaded', () => {
  const carousels = document.querySelectorAll('.carousel');
  carousels.forEach(carousel => {
    const viewport = carousel.querySelector('.carousel-viewport');
    const track = carousel.querySelector('.carousel-track');
    const cells = Array.from(carousel.querySelectorAll('.carousel-cell'));
    const prev = carousel.querySelector('.carousel-btn.prev');
    const next = carousel.querySelector('.carousel-btn.next');

    if (!viewport || !track || cells.length === 0) return;

    const gap = () => parseFloat(getComputedStyle(track).gap) || 20;
    let cellWidth = Math.round(cells[0].getBoundingClientRect().width + gap());
    const recompute = () => {
      cellWidth = Math.round(cells[0].getBoundingClientRect().width + gap());
    };
    // Recompute on resize or when images finish loading
    window.addEventListener('resize', () => { recompute(); setPosition(true); });
    cells.forEach(c => {
      const img = c.querySelector('img');
      if (img && !img.complete) img.addEventListener('load', () => { recompute(); setPosition(true); });
    });

    // ---- Looping carousel using clones + transform ----
    // Clone first and last cells to create the infinite loop illusion
    const firstCell = cells[0];
    const lastCell = cells[cells.length - 1];
    const firstClone = firstCell.cloneNode(true);
    const lastClone = lastCell.cloneNode(true);
    track.appendChild(firstClone);
    track.insertBefore(lastClone, track.firstChild);

    // Refresh cells NodeList after cloning
    let allCells = Array.from(track.querySelectorAll('.carousel-cell'));

    // currentIndex refers to allCells; start at 1 (first real item)
    let currentIndex = 1;
    // set initial transform
    track.style.transition = 'transform 300ms ease';
    const setPosition = (instant = false) => {
      if (instant) track.style.transition = 'none';
      else track.style.transition = 'transform 300ms ease';
      track.style.transform = `translateX(-${currentIndex * cellWidth}px)`;
      if (instant) requestAnimationFrame(() => { track.style.transition = 'transform 300ms ease'; });
    };

    // ensure viewport scrollLeft is 0 and set track width/layout
    // Important: force reflow to get sizes
    recompute();
    setPosition(true);

    const moveToIndex = (index) => {
      currentIndex = index;
      setPosition();
    };

    if (next) next.addEventListener('click', () => {
      if (currentIndex >= allCells.length - 1) return; // protection
      moveToIndex(currentIndex + 1);
    });

    if (prev) prev.addEventListener('click', () => {
      if (currentIndex <= 0) return;
      moveToIndex(currentIndex - 1);
    });

    // when transition ends, if we're on a clone, jump to the real one without animation
    track.addEventListener('transitionend', () => {
      allCells = Array.from(track.querySelectorAll('.carousel-cell'));
      // If we're at the appended firstClone (last index), jump to real first (index 1)
      if (allCells[currentIndex].isSameNode(firstClone)) {
        currentIndex = 1;
        setPosition(true);
      }
      // If we're at the prepended lastClone (index 0), jump to last real
      if (allCells[currentIndex].isSameNode(lastClone)) {
        currentIndex = allCells.length - 2;
        setPosition(true);
      }
    });

    // Click on cell toggles caption; mouseleave hides it (apply to all cells incl. clones)
    allCells.forEach(cell => {
      const img = cell.querySelector('img');
      // create caption element from data-description if not present
      let caption = cell.querySelector('.caption');
      if (!caption) {
        caption = document.createElement('div');
        caption.className = 'caption';
        // Format the description text with line breaks
        const description = img?.getAttribute('data-description') || '';
        // 1. Remplacer les '|' par des sauts de ligne
        // 2. Remplacer les espaces avant ':' par des sauts de ligne
        // 3. Gérer les '\n' explicites
        const formattedText = description
            .replace(/\|/g, '\n')
            .replace(/(\w+):/g, '\n$1:')
            .replace(/\\n/g, '\n')
            .trim();
        caption.textContent = formattedText;
        cell.appendChild(caption);
      }

      cell.addEventListener('click', (e) => {
        // toggle only when clicking the cell (not the buttons)
        cell.classList.toggle('show');
      });

      cell.addEventListener('mouseleave', () => {
        cell.classList.remove('show');
      });
    });
  });
});