document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.form-input').forEach(input => {
        const blockId = input.parentElement.id;
        const label = input.previousElementSibling;

        if(input.value) {
            document.getElementById(blockId).classList.add('active');
            label.classList.add('active');
        }

        input.addEventListener('focus', () => {
            document.getElementById(blockId).classList.add('active');
            label.classList.add('active');
        });

        input.addEventListener('blur', () => {
            if (!input.value) {
                document.getElementById(blockId).classList.remove('active');
                label.classList.remove('active');
            }
        });
    });

    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0
    let yyyy = today.getFullYear();

    const minDate = `${yyyy}-${mm}-${dd}T00:00`; // Template literal for clarity
    const dateInput = document.getElementById('id_unsealing_date');

    if (dateInput) {
        dateInput.setAttribute("min", minDate);
    }

    let modal = document.getElementById("capsuleFormModal"); // Get the modal
    let btn = document.querySelector("button[data-target='#capsuleFormModal']");  // Get the button that opens the modal
    let span = document.getElementsByClassName("close")[0];  // Get the <span> element that closes the modal
    function resetFormFields() {
        document.getElementById('id_name').value = '';
        document.getElementById('nameBlock').classList.remove('active');
        document.getElementById('nameLabel').classList.remove('active');

        document.getElementById('id_description').value = '';
        document.getElementById('descriptionBlock').classList.remove('active');
        document.getElementById('descriptionLabel').classList.remove('active');

        document.getElementById('id_unsealing_date').value = ''; // Set to today's date or leave blank
        document.getElementById('unsealing_dateBlock').classList.remove('active');
        document.getElementById('unsealing_dateLabel').classList.remove('active');

        document.getElementById('id_is_public').value = 'False';

        document.getElementById('id_is_published').value = 'False';

        // Clear the uploaded files list UI and the arrays tracking the files
        const fileListContainer = document.querySelector('.new-uploaded-capsule-content-section');
        fileListContainer.innerHTML = '';
        selectedFiles = [];
        filesToDelete = [];

        updateFileListDisplay();

        // Change the button text to "Submit"
        document.getElementById('form-button').textContent = 'Submit';
        document.getElementById('capsule-form-header').textContent = 'Create your Time Capsule!';
    }
    // When the user clicks the button, open the modal
    if(btn != null) { // Check if the button was found
        btn.onclick = function() {
            resetFormFields();
            modal.style.display = "flex";
        }
    }
    // When the user clicks on <span> (x), close the modal
    if(span != null) { // Check if the span was found
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

    // Drag and Drop functionality
    const form = document.getElementById('capsuleForm');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('capsule_contents');
    const submitButton = document.getElementById('form-button');
    const fileListContainer = document.querySelector('.uploaded-capsule-content-section');
    let selectedFiles = []; // To keep track of the selected files

    // Function to update the displayed file list
    function updateFileListDisplay() {
        fileListContainer.innerHTML = ''; // Clear current list
        if (selectedFiles.length < 0) {
            // Reset styles if no files are selected
            fileListContainer.style.background = 'none';
            fileListContainer.style.padding = '0';
        }
       if (selectedFiles.length > 0) {
           submitButton.disabled = false;
       } else {
           submitButton.disabled = true;
       }
       updateSubmitButtonState();
        selectedFiles.forEach((file, index) => {
            const fileElement = document.createElement('div');
            fileElement.className = 'file-item';

            const fileName = document.createElement('span');
            fileName.textContent = file.name;
            fileName.className = 'file-item'; // Add a class for styling

            const deleteIcon = document.createElement('span');
            deleteIcon.textContent = 'X';
            deleteIcon.className = 'delete-icon';
            deleteIcon.addEventListener('click', () => {
                selectedFiles = selectedFiles.filter((_, i) => i !== index); // Remove the file from the array
                updateFileListDisplay(); // Refresh the displayed file list
            });
            fileElement.appendChild(fileName);
            fileElement.appendChild(deleteIcon);
            fileListContainer.appendChild(fileElement);
        });
    }

    // Handle files after selection or drop
    function handleFiles(files) {
        const dropZoneText = document.getElementById('dropZone').querySelector('p'); // Assuming your dropzone has a <p> tag for text
        const originalText = dropZoneText.textContent; // Save the original text
        dropZoneText.innerHTML = '<div class="spinner"></div>'; // Add your spinner HTML here
        selectedFiles = selectedFiles.concat(Array.from(files)); // Add new files to the array
        setTimeout(() => {
            updateFileListDisplay(); // Update the list display
            dropZoneText.textContent = originalText;
            fileInput.value = '';
        }, 500); // Adjust the delay as necessary
    }

    // Open file dialog when dropZone is clicked
    dropZone.addEventListener('click', () => fileInput.click());

    // Update selected files when user selects files
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    // Handle file drop
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    // Prevent default behavior for dragover
    dropZone.addEventListener('dragover', (e) => e.preventDefault());

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent normal form submission

        const formData = new FormData(this);
        selectedFiles.forEach((file) => {
            formData.append('capsule_contents', file);
        });

        // Append files marked for deletion
        filesToDelete.forEach(fileId => {
            formData.append('filesToDelete', fileId);
        });

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken },
            credentials: 'include',
        })
        .then(response => response.text())
        .then(data => {
            console.log(data); // For debugging
            const [status, message] = data.split('|');
            if(status === 'success') {
                window.location.href = message;  // Redirect to the given URL
                filesToDelete = [];
            } else {
                console.error('Error:', message)
            }
        })
        .catch(error => console.error('Error:', error));
    });

    let filesToDelete = [];

    function markForDeletion(fileId, element) {
        // Add the fileId to the list of files to be deleted
        filesToDelete.push(fileId);
        // Remove the file element from the UI as visual feedback
        element.parentNode.remove();
        updateSubmitButtonState();
    }

    let initialExistingFilesCount = 0;

    function updateSubmitButtonState() {
        const totalValidFileCount = initialExistingFilesCount - filesToDelete.length + selectedFiles.length;
        submitButton.disabled = totalValidFileCount <= 0;
    }

    function populateExistingFiles(capsuleId) {
        fetch(`/capsule-contents/${capsuleId}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const fileListContainer = document.querySelector('.new-uploaded-capsule-content-section');
                fileListContainer.innerHTML = ''; // Clear current list
                initialExistingFilesCount = data.length;
                data.forEach((content) => {
                    const fileElement = document.createElement('div');
                    fileElement.className = 'file-item';
                    const fileName = document.createElement('span');
                    fileName.textContent = content.file.split('/').pop(); // Adjust according to your response structure
                    const deleteIcon = document.createElement('span');
                    deleteIcon.textContent = 'del';
                    deleteIcon.className = 'delete-icon';
                    deleteIcon.onclick = () => markForDeletion(content.id, deleteIcon); // Implement this function
                    fileElement.appendChild(fileName);
                    fileElement.appendChild(deleteIcon);
                    fileListContainer.appendChild(fileElement);
                });
                updateSubmitButtonState();
                console.log(data);
            })
            .catch(error => console.error('Error:', error));
    }

    // Function to open and populate the modal for editing
    document.querySelectorAll('.edit-icon').forEach(button => {
        button.addEventListener('click', function() {
            const capsuleId = this.getAttribute('data-capsule-id');
            // Reset any previous state
            resetFormFields();
            selectedFiles = [];
            filesToDelete = [];

            fetch(`/edit/${capsuleId}/`, { method: 'GET', credentials: 'include' })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    document.getElementById('form-button').textContent = 'Update';
                    document.getElementById('capsule-form-header').textContent = 'Update your Time Capsule';
                    // Populate the form fields with the capsule data
                    document.getElementById('nameBlock').classList.add('active');
                    document.getElementById('nameLabel').classList.add('active');
                    document.getElementById('id_name').value = data.name;

                    document.getElementById('descriptionBlock').classList.add('active');
                    document.getElementById('descriptionLabel').classList.add('active');
                    document.getElementById('id_description').value = data.description;

                    document.getElementById('unsealing_dateBlock').classList.add('active');
                    document.getElementById('unsealing_dateLabel').classList.add('active');
                    document.getElementById('id_unsealing_date').value = data.unsealing_date;

                    let is_public = data.is_public ? 'True' : 'False';
                    document.getElementById('id_is_public').value = is_public;

                    let is_published = data.is_published ? 'True' : 'False';
                    document.getElementById('id_is_published').value = is_published;

                    // Change the form action to update the capsule
                    document.querySelector('#capsuleForm').action = `/edit/${capsuleId}/`;
                    modal.style.display = "flex";  // Open the modal

                    populateExistingFiles(capsuleId);
                })
                .catch(error => console.error('Error:', error));
        });
    });
});