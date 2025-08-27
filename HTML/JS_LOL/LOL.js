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

function afficherImage()
{
    var imgZoom = document.querySelector('.modal');
    var modalImage = document.querySelector('.modalImage');

    Array.from(document.querySelectorAll('.zoom')).forEach(
      item => {item.addEventListener("click", event =>{
        imgZoom.style.display="block";
      modalImage.src=event.target.src
    } );
  });

  document.querySelector(".close").addEventListener("click", () => {
imgZoom.style.display="none";
  });

}



