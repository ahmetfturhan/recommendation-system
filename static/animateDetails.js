let card = [...document.querySelectorAll('.card')];
let detailsBtn = [...document.querySelectorAll('.details_btn')];
let front = [...document.querySelectorAll('.frontside')];
let backDetail = [...document.querySelectorAll('.backside_details')];
let backBtn = [...document.querySelectorAll('.back_btn_details')];




detailsBtn.forEach((item, i) => {
    detailsBtn[i].addEventListener('click', () => {
      card[i].style.transform = 'rotateY(180deg)';
      card[i].style.transitionDelay = '0.4s';
      
      front[i].style.visibility = 'hidden';
      
      backDetail[i].style.visibility = 'visible';
      backDetail[i].style.transitionDelay = '0.6s';
      
      // hide the comment button and show the back button
      
    })
  })
  
  backBtn.forEach((item, i) => {
    backBtn[i].addEventListener('click', () => {
      card[i].style.transform = 'rotateY(0deg)';
      card[i].style.transitionDelay = '0.4s';
      
      backDetail[i].style.visibility = 'hidden';
  
      front[i].style.visibility = 'visible';
      front[i].style.transitionDelay = '0.6s';
      
      
      
      // hide the back button and show the comment button
     
    })
  })