let card = [...document.querySelectorAll('.card')];
let detailsBtn = [...document.querySelectorAll('.details_btn')];
let commentBtn = [...document.querySelectorAll('.comment-btn')];
let front = [...document.querySelectorAll('.frontside')];
let backDetail = [...document.querySelectorAll('.backside_details')];
let backComment = [...document.querySelectorAll('.backside-comments')];
let backBtn = [...document.querySelectorAll('.back_btn')];
let backBtnDetails = [...document.querySelectorAll('.back_btn_details')];


detailsBtn.forEach((item, i) => {
  detailsBtn[i].addEventListener('click', () => {
    card[i].style.transform = 'rotateY(180deg)';
    card[i].style.transitionDelay = '0.4s';

    front[i].style.visibility = 'hidden';

    backDetail[i].style.visibility = 'visible';
    backDetail[i].style.transitionDelay = '0.6s';

    // hide the comment button and show the back button
    //detailsBtn[i].style.display = 'none';
    backBtnDetails[i].style.display = 'block';
  });
});

commentBtn.forEach((item, i) => {
  commentBtn[i].addEventListener('click', () => {
    card[i].style.transform = 'rotateY(180deg)';
    card[i].style.transitionDelay = '0.4s';

    front[i].style.visibility = 'hidden';

    backComment[i].style.visibility = 'visible';
    backComment[i].style.transitionDelay = '0.6s';

    // hide the comment button and show the back button
    //commentBtn[i].style.display = 'none';
    backBtn[i].style.display = 'block';
  });
});

backBtn.forEach((item, i) => {
  backBtn[i].addEventListener('click', () => {
    card[i].style.transform = 'rotateY(0deg)';
    card[i].style.transitionDelay = '0.4s';

    backComment[i].style.visibility = 'hidden';

    front[i].style.visibility = 'visible';
    front[i].style.transitionDelay = '0.6s';

    // hide the back button and show the comment button
    backBtn[i].style.display = 'none';
    //commentBtn[i].style.display = 'block';
  });
});


backBtnDetails.forEach((item, i) => {
    backBtnDetails[i].addEventListener('click', () => {
      card[i].style.transform = 'rotateY(0deg)';
      card[i].style.transitionDelay = '0.4s';
  
      backDetail[i].style.visibility = 'hidden';
  
      front[i].style.visibility = 'visible';
      front[i].style.transitionDelay = '0.6s';
  
      // hide the back button and show the comment button
      backBtnDetails[i].style.display = 'none';
      //detailsBtn[i].style.display = 'block';
    });
  });
