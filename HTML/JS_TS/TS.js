function changerCouleurNav()
{
    var navHidden = document.getElementById('navHidden');
    var scrollValue = window.scrollY;

    if(scrollValue < 500){
      navHidden.classList.remove('navShow');
    }else{
      navHidden.classList.add('navShow');
    }
}

window.addEventListener('scroll', changerCouleurNav);


//Deuxieme fonction Image

// function afficherImage()
// {
//     var imgZoom = document.querySelector('.modal');
//     var modalImage = document.querySelector('.modalImage');

//     Array.from(document.querySelectorAll('.zoom')).forEach(
//       item => {item.addEventListener("click", event =>{
//         imgZoom.style.display="block";
//       modalImage.src=event.target.src
//     } );
//   });

//   document.querySelector(".close").addEventListener("click", () => {
// imgZoom.style.display="none";
//   });

// }


document.addEventListener("DOMContentLoaded", () => {
  let sections = document.querySelectorAll("#multimediaContact, #GitHub_VS_Apache_Nginx, #formulaireContact", "#navbarInferieur");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("afficher");
      }
    });
  }, { threshold: 0.1 });

  sections.forEach(section => {
    console.log("Section trouvée :", section.id);
    observer.observe(section);
  });
});

