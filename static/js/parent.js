$(document).ready(() => {
	$(".save_username_parent").click((e) => {
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
						url: "/parent/account/username",
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

	$(".save_password_parent").click((e) => {
		e.preventDefault();

		var parentCurrentPassowrd = $(".parent_currentPassowrd").val();
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
						url: "/parent/account/password",
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
