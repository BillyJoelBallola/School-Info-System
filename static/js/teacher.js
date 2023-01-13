$(document).ready(function () {
	$(".save_btn").click(function (e) {
		e.preventDefault();

		var title = $(".announcement_title").val();
		var audience = $(".announcement_audience").val();
		var purpose = $(".announcement_purpose").val();
		var place = $(".announcement_place").val();
		var date = $(".announcement_date").val();

		if (
			title == "" ||
			audience == "" ||
			purpose == "" ||
			place == "" ||
			date == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			swal({
				title: "Are you sure?",
				text: "Once added, this announcement cannot be change.",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willAdd) => {
				if (willAdd) {
					$.ajax({
						type: "POST",
						url: "/teacher/announcements",
						data: {
							title: title,
							audience: audience,
							purpose: purpose,
							place: place,
							date: date,
						},
						success: function (response) {
							swal("Accouncement added successfully", {
								icon: "success",
							}).then((result) => {
								location.reload();
							});
						},
						error: function (response) {
							swal("Adding annoucement failed", {
								icon: "error",
							}).then((result) => {
								location.reload();
							});
						},
					});
				}
			});
		}
	});

	$(".archive_announcement_btn").click(function (e) {
		e.preventDefault();

		var annoucement_id = $(this)
			.closest(".announcement-title-control")
			.find(".announcement_id")
			.val();

		swal({
			title: "Are you sure?",
			text: "Once archive, this announcement cannot be restored",
			icon: "warning",
			buttons: true,
			dangerMode: true,
		}).then((willEdit) => {
			if (willEdit) {
				$.ajax({
					type: "POST",
					url: `/teacher/announcements/archive/${annoucement_id}`,
					success: function (response) {
						swal("Announcement archive successfully", {
							icon: "success",
						}).then((result) => {
							location.reload();
						});
					},
					error: function (response) {
						swal("Failed to archive this announcement", {
							icon: "error",
						}).then((result) => {
							location.reload();
						});
					},
				});
			}
		});
	});

	$(".save_username_teacher").click((e) => {
		e.preventDefault();

		var newUsername = $("#username").val();
		var password = $("#password").val();

		if (newUsername == "" || password == "") {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you want to change your username?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willSubmit) => {
				if (willSubmit) {
					$.ajax({
						type: "POST",
						url: "/teacher/account/username",
						data: {
							newUsername: newUsername,
							password: password,
						},
						success: function (response) {
							swal("Username changed successfully", {
								icon: "success",
							}).then((result) => {
								window.location.href = "/login";
							});
						},
						error: function (response) {
							swal("Incorrect password", {
								icon: "error",
							}).then((result) => {
								location.reload();
							});
						},
					});
				}
			});
		}
	});

	$(".save_password_teacher").click((e) => {
		e.preventDefault();

		var parentCurrentPassowrd = $(".teacher_current_password").val();
		var currentPassword = $("#currentpassword").val();
		var newPassword = $("#newpassword").val();
		var confirmPassword = $("#confirmpassword").val();

		if (currentPassword == "" || newPassword == "" || confirmPassword == "") {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else if (newPassword != confirmPassword) {
			swal("Password did not match", {
				icon: "error",
			});
		} else if (parentCurrentPassowrd != currentPassword) {
			swal("Current password incorrect", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you want to change your password?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willSubmit) => {
				if (willSubmit) {
					$.ajax({
						type: "POST",
						url: "/teacher/account/password",
						data: {
							confirmPassword: confirmPassword,
						},
						success: function (response) {
							swal("Password changed successfully", {
								icon: "success",
							}).then((result) => {
								window.location.href = "/login";
							});
						},
						error: function (response) {
							swal("Something went wrong, failed to change password", {
								icon: "error",
							}).then((result) => {
								location.reload();
							});
						},
					});
				}
			});
		}
	});
});
