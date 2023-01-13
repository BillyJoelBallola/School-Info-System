$(document).ready(function () {
	$(".login_btn").click(function (e) {
		e.preventDefault();

		var username = $(".username").val();
		var password = $(".password").val();
		var accType = $(".accType").val();

		if (username == "" || password == "") {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else if (accType == "") {
			swal("Choose account type", {
				icon: "error",
			});
		} else {
			$.ajax({
				type: "POST",
				url: "/login",
				data: {
					username: username,
					password: password,
					accType: accType,
				},
				success: function (response) {
					swal("login success", {
						icon: "success",
					}).then((result) => {
						if (accType == "Parent") {
							document.location.href = "/parent/home";
						} else if (accType == "Teacher") {
							document.location.href = "/teacher/home";
						} else if (accType == "Admin") {
							document.location.href = "/admin/home";
						}
					});
				},
				error: function (response) {
					swal("User not found", {
						icon: "error",
					});
				},
			});
		}
	});

	$(".register_btn").click(function (e) {
		e.preventDefault();

		function removeSpaces(array) {
			const lname = array[1].split(" ").join("");
			const mname = array[2].split(" ").join("");
			array.pop(2);
			array.pop(2);
			array.push(lname, mname);
		}

		var childName = $(".childName").val();
		var parentFirstName = $(".parentFirstName").val();
		var parentLastName = $(".parentLastName").val();
		var username = $(".username").val();
		var createPassword = $(".createPassword").val();
		var confirmPassword = $(".confirmPassword").val();

		const childNameArray = childName.split(",");
		removeSpaces(childNameArray);

		if (
			childName == "" ||
			parentFirstName == "" ||
			parentLastName == "" ||
			username == "" ||
			createPassword == "" ||
			confirmPassword == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else if (createPassword != confirmPassword) {
			swal("Password did not match", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you register this information?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willRegister) => {
				if (willRegister) {
					$.ajax({
						type: "POST",
						url: `/register`,
						data: {
							childFname: childNameArray[0],
							childLname: childNameArray[1],
							childMname: childNameArray[2],
							parentFirstName: parentFirstName,
							parentLastName: parentLastName,
							username: username,
							createPassword: createPassword,
						},
						success: function (response) {
							swal("Parent account successfully created", {
								icon: "success",
							}).then((result) => {
								window.location.href = "/login";
							});
						},
						error: function (response) {
							swal("Child's name does not exist in the student list", {
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
