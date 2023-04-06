let card = [...document.querySelectorAll('.card')];
let commentBtn = [...document.querySelectorAll('.comment-btn')];
let front = [...document.querySelectorAll('.frontside')];
let backComment = [...document.querySelectorAll('.backside-comments')];
let backBtn = [...document.querySelectorAll('.back_btn')];

commentBtn.forEach((item, i) => {
  commentBtn[i].addEventListener('click', () => {
    card[i].style.transform = 'rotateY(180deg)';
    card[i].style.transitionDelay = '0.4s';
    
    front[i].style.visibility = 'hidden';
    
    backComment[i].style.visibility = 'visible';
    backComment[i].style.transitionDelay = '0.6s';
    
    // hide the comment button and show the back button
    
  })
})

backBtn.forEach((item, i) => {
  backBtn[i].addEventListener('click', () => {
    card[i].style.transform = 'rotateY(0deg)';
    card[i].style.transitionDelay = '0.4s';
    
    backComment[i].style.visibility = 'hidden';

    front[i].style.visibility = 'visible';
    front[i].style.transitionDelay = '0.6s';
    
    
    
    // hide the back button and show the comment button
   
  })
})
