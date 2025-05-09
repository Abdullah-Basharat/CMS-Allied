document.addEventListener("DOMContentLoaded", function () {
  // Form validation
  const forms = document.querySelectorAll(".needs-validation");
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      },
      false
    );
  });

  // Delete confirmation
  const deleteButtons = document.querySelectorAll("[data-delete-url]");
  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const deleteUrl = this.dataset.deleteUrl;
      const deleteForm = document.getElementById("deleteForm");
      deleteForm.action = deleteUrl;
    });
  });

  // Grade modal handling
  const gradeButtons = document.querySelectorAll("[data-grade-id]");
  gradeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const gradeId = this.dataset.gradeId;
      // Fetch grade data and populate modal
      fetch(`/api/grades/${gradeId}/`)
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("first_term_marks").value =
            data.first_term_marks;
          document.getElementById("second_term_marks").value =
            data.second_term_marks;
          document.getElementById("final_marks").value = data.final_marks;
          document.getElementById(
            "gradeForm"
          ).action = `/grades/${gradeId}/update/`;
        });
    });
  });

  // Attendance marking
  const attendanceButtons = document.querySelectorAll("[data-record-id]");
  attendanceButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const recordId = this.dataset.recordId;
      // Fetch attendance data and populate modal
      fetch(`/api/attendance/${recordId}/`)
        .then((response) => response.json())
        .then((data) => {
          // Populate attendance modal
        });
    });
  });

  // Enable Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Enable Bootstrap popovers
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Auto-hide alerts after 5 seconds
  setTimeout(function () {
    var alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
      var bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);
});
