function closeModal(modal_id){
  const modal = document.getElementById(modal_id)
  modal.style.display='none';
}

function openModal(modal_id) {
  const modal = document.getElementById(modal_id);
  modal.style.display='block';
}