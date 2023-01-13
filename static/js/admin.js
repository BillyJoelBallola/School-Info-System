$(document).ready(function () {
	//article
	$(".save_article_btn").click(function (e) {
		e.preventDefault();

		var form_data = new FormData();

		var article_title = $(".article_title").val();
		var article_date = $(".article_date").val();
		var article_content = $(".article_content").val();
		let article_img = $(".article_img")[0].files[0];

		form_data.append("title", article_title);
		form_data.append("date", article_date);
		form_data.append("content", article_content);
		form_data.append("img", article_img);

		if (article_img != null) {
			var article_img_name = article_img["name"];
			var valid_extentions = ["png", "jpg", "jpeg"];
			var fileNameExt = article_img_name.substr(
				article_img_name.lastIndexOf(".") + 1
			);
		}

		if (
			article_title == "" ||
			article_date == "" ||
			article_content == "" ||
			article_img == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else if ($.inArray(fileNameExt, valid_extentions) == -1) {
			swal("Invalid file type", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you want to add this article?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willAdd) => {
				if (willAdd) {
					$.ajax({
						type: "POST",
						url: "/admin/articles",
						contentType: false,
						processData: false,
						data: form_data,
						success: function (response) {
							swal("Article added successfully", {
								icon: "success",
							}).then((result) => {
								location.reload();
							});
						},
						error: function (response) {
							swal("Adding article failed", {
								icon: "error",
							});
						},
					});
				}
			});
		}
	});

	$(".edit_article_btn").click(function (e) {
		e.preventDefault();

		var form_data = new FormData();

		var article_id = $(".article_id").val();
		var article_title_edit = $(".article_title").val();
		var article_date_edit = $(".article_date").val();
		var article_content_edit = $(".article_content").val();
		var article_img_current = $(".article_img_current").val();
		let article_img_new = $(".article_img")[0].files[0];

		let article_img_edit = "";

		if (article_img_new != null) {
			var article_img_name = article_img_new["name"];
			var valid_extentions = ["png", "jpg", "jpeg"];
			var fileNameExt = article_img_name.substr(
				article_img_name.lastIndexOf(".") + 1
			);
			article_img_edit = article_img_new;
		} else {
			article_img_edit = article_img_current;
		}

		if ($.inArray(fileNameExt, valid_extentions) == -1) {
			swal("Invalid file type", {
				icon: "error",
			});
		}

		form_data.append("title", article_title_edit);
		form_data.append("date", article_date_edit);
		form_data.append("content", article_content_edit);
		form_data.append("current_img", article_img_current);
		form_data.append("img", article_img_edit);

		if (
			article_title_edit == "" ||
			article_date_edit == "" ||
			article_content_edit == "" ||
			article_img_current == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you want to edit this article?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willEdit) => {
				if (willEdit) {
					$.ajax({
						type: "POST",
						url: `/admin/articles/edit_save/${article_id}`,
						contentType: false,
						processData: false,
						data: form_data,
						success: function (response) {
							swal("Article edited successfully", {
								icon: "success",
							}).then((result) => {
								window.location.href = "/admin/articles";
							});
						},
						error: function (response) {
							swal("Saving edited article failed", {
								icon: "error",
							});
						},
					});
				}
			});
		}
	});

	$(".delete_article_btn").click(function (e) {
		e.preventDefault();

		var item_id = $(this).closest("tr").find(".article_id").val();

		swal({
			text: "Are you sure you want to delete this article?",
			icon: "warning",
			buttons: true,
			dangerMode: true,
		}).then((willDelete) => {
			if (willDelete) {
				$.ajax({
					type: "POST",
					url: "/admin/delete/article",
					data: {
						item_id: item_id,
					},
					success: function (response) {
						swal("Article deleted successfully", {
							icon: "success",
						}).then((result) => {
							location.reload();
						});
					},
					error: function (response) {
						swal("Deleting article failed", {
							icon: "error",
						}).then((result) => {
							location.reload();
						});
					},
				});
			}
		});
	});

	// events
	$(".save_event_btn").click(function (e) {
		e.preventDefault();

		var form_data = new FormData();

		var event_title = $(".event_title").val();
		var event_date = $(".event_date").val();
		var event_content = $(".event_content").val();
		let event_img = $(".event_img")[0].files[0];

		form_data.append("title", event_title);
		form_data.append("date", event_date);
		form_data.append("content", event_content);
		form_data.append("img", event_img);

		if (event_img != null) {
			var event_img_name = event_img["name"];
			var valid_extentions = ["png", "jpg", "jpeg"];
			var fileNameExt = event_img_name.substr(
				event_img_name.lastIndexOf(".") + 1
			);
		}

		if (
			event_title == "" ||
			event_date == "" ||
			event_content == "" ||
			event_img == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else if ($.inArray(fileNameExt, valid_extentions) == -1) {
			swal("Invalid file type", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you want to add this event?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willAdd) => {
				if (willAdd) {
					$.ajax({
						type: "POST",
						url: "/admin/events",
						contentType: false,
						processData: false,
						data: form_data,
						success: function (response) {
							swal("Event added successfully", {
								icon: "success",
							}).then((result) => {
								location.reload();
							});
						},
						error: function (response) {
							swal("Adding event failed", {
								icon: "error",
							});
						},
					});
				}
			});
		}
	});

	$(".edit_event_btn").click(function (e) {
		e.preventDefault();

		var form_data = new FormData();

		var event_id = $(".event_id").val();
		var event_title_edit = $(".event_title").val();
		var event_date_edit = $(".event_date").val();
		var event_content_edit = $(".event_content").val();
		var event_img_current = $(".event_img_current").val();
		let event_img_new = $(".event_img")[0].files[0];

		let event_img_edit = "";

		if (event_img_new != null) {
			var event_img_name = event_img_new["name"];
			var valid_extentions = ["png", "jpg", "jpeg"];
			var fileNameExt = event_img_name.substr(
				event_img_name.lastIndexOf(".") + 1
			);
			event_img_edit = event_img_new;
		} else {
			event_img_edit = event_img_current;
		}

		if ($.inArray(fileNameExt, valid_extentions) == -1) {
			swal("Invalid file type", {
				icon: "error",
			});
		}

		form_data.append("title", event_title_edit);
		form_data.append("date", event_date_edit);
		form_data.append("content", event_content_edit);
		form_data.append("current_img", event_img_current);
		form_data.append("img", event_img_edit);

		if (
			event_title_edit == "" ||
			event_date_edit == "" ||
			event_content_edit == "" ||
			event_img_current == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you want to edit this event?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willEdit) => {
				if (willEdit) {
					$.ajax({
						type: "POST",
						url: `/admin/events/edit_save/${event_id}`,
						contentType: false,
						processData: false,
						data: form_data,
						success: function (response) {
							swal("Event edited successfully", {
								icon: "success",
							}).then((result) => {
								window.location.href = "/admin/events";
							});
						},
						error: function (response) {
							swal("Saving edited event failed", {
								icon: "error",
							});
						},
					});
				}
			});
		}
	});

	$(".delete_event_btn").click(function (e) {
		e.preventDefault();

		var item_id = $(this).closest("tr").find(".event_id").val();

		swal({
			text: "Are you sure you want to delete this event?",
			icon: "warning",
			buttons: true,
			dangerMode: true,
		}).then((willDelete) => {
			if (willDelete) {
				$.ajax({
					type: "POST",
					url: "/admin/delete/event",
					data: {
						item_id: item_id,
					},
					success: function (response) {
						swal("Event deleted successfully", {
							icon: "success",
						}).then((result) => {
							location.reload();
						});
					},
					error: function (response) {
						swal("Deleting event failed", {
							icon: "error",
						}).then((result) => {
							location.reload();
						});
					},
				});
			}
		});
	});

	// announcements
	$(".save_announcement_btn").click(function (e) {
		e.preventDefault();

		var title = $(".announcement_title").val();
		var audience = $(".announcement_audience").val();
		var purpose = $(".announcement_purpose").val();
		var place = $(".announcement_place").val();
		var date = $(".announcement_date").val();

		if (
			title == "" ||
			purpose == "" ||
			audience == "" ||
			place == "" ||
			date == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			swal({
				title: "Are you sure?",
				text: "Once added, you cannot edit the content of this annoucement",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willAdd) => {
				if (willAdd) {
					$.ajax({
						type: "POST",
						url: "/admin/announcements",
						data: {
							title: title,
							purpose: purpose,
							audience: audience,
							place: place,
							date: date,
						},
						success: function (response) {
							swal("Announcement added successfully", {
								icon: "success",
							}).then((result) => {
								location.reload();
							});
						},
						error: function (response) {
							swal("Adding announcement failed", {
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

		var annoucement_id = $(this).closest("tr").find(".announcement_id").val();

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
					url: `/admin/announcements/archive/${annoucement_id}`,
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

	// students
	$(".save_student_btn").click(function (e) {
		e.preventDefault();

		var form_data = new FormData();
		var fname = $(".student_fname").val();
		var lname = $(".student_lname").val();
		var mname = $(".student_mname").val();
		var dob = $(".student_dob").val();
		var age = $(".student_age").val();
		var lrn = $(".student_lrn").val();
		var grade = $(".student_grade").val();
		var section = $(".student_section").val();
		var address = $(".student_address").val();

		if (
			fname == "" ||
			lname == "" ||
			mname == "" ||
			dob == "" ||
			age == "" ||
			lrn == "" ||
			grade == "" ||
			section == "" ||
			address == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			form_data.append("fname", fname);
			form_data.append("lname", lname);
			form_data.append("mname", mname);
			form_data.append("dob", dob);
			form_data.append("age", age);
			form_data.append("lrn", lrn);
			form_data.append("grade", grade);
			form_data.append("section", section);
			form_data.append("address", address);

			swal({
				text: "Are you sure you want to add this student information?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willAdd) => {
				if (willAdd) {
					$.ajax({
						type: "POST",
						url: "/admin/students",
						contentType: false,
						processData: false,
						data: form_data,
						success: function (response) {
							swal("Student information added successfully", {
								icon: "success",
							}).then((result) => {
								location.reload();
							});
						},
						error: function (response) {
							swal("Student information already existing", {
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

	$(".archive_students_btn").click(function (e) {
		e.preventDefault();

		var student_id = $(this).closest("tr").find(".student_id").val();

		swal({
			title: "Are you sure?",
			text: "Once archive, this student info cannot be restored",
			icon: "warning",
			buttons: true,
			dangerMode: true,
		}).then((willEdit) => {
			if (willEdit) {
				$.ajax({
					type: "POST",
					url: `/admin/students/archive/${student_id}`,
					success: function (response) {
						swal("Student info archive successfully", {
							icon: "success",
						}).then((result) => {
							location.reload();
						});
					},
					error: function (response) {
						swal("Failed to archive this student info", {
							icon: "error",
						}).then((result) => {
							location.reload();
						});
					},
				});
			}
		});
	});

	// edit student
	$(".student_edit_lrn_btn").click(function (e) {
		e.preventDefault();

		swal("Enter student's LRN that want to edit:", {
			content: "input",
		}).then((lrn) => {
			if (lrn) {
				$.ajax({
					type: "POST",
					url: `/admin/students/edit/${lrn}`,
					success: function (response) {
						swal("Student's info found", {
							icon: "success",
						}).then((result) => {
							window.location.href = `/admin/students/edit/${lrn}`;
						});
					},
					error: function (response) {
						swal("Student's info not found", {
							icon: "error",
						}).then((result) => {
							location.reload();
						});
					},
				});
			} else {
				swal("Student's info not found", {
					icon: "error",
				});
			}
		});
	});

	$(".save_student_edit_btn").click(function (e) {
		e.preventDefault();

		var form_data = new FormData();

		var stud_id = $(".student_id_edit").val();
		var fname = $(".student_fname_edit").val();
		var lname = $(".student_lname_edit").val();
		var mname = $(".student_mname_edit").val();
		var dob = $(".student_dob_edit").val();
		var age = $(".student_age_edit").val();
		var lrn = $(".student_lrn_edit").val();
		var grade = $(".student_grade_edit").val();
		var section = $(".student_section_edit").val();
		var address = $(".student_address_edit").val();

		if (
			fname == "" ||
			lname == "" ||
			mname == "" ||
			dob == "" ||
			age == "" ||
			lrn == "" ||
			grade == "" ||
			section == "" ||
			address == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			form_data.append("stud_id", stud_id);
			form_data.append("fname", fname);
			form_data.append("lname", lname);
			form_data.append("mname", mname);
			form_data.append("dob", dob);
			form_data.append("age", age);
			form_data.append("lrn", lrn);
			form_data.append("grade", grade);
			form_data.append("section", section);
			form_data.append("address", address);

			swal({
				text: "Are you sure you want to edit this student information?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willEdit) => {
				if (willEdit) {
					$.ajax({
						type: "POST",
						url: `/admin/students/update`,
						contentType: false,
						processData: false,
						data: form_data,
						success: function (response) {
							swal("Student information edited successfully", {
								icon: "success",
							}).then((result) => {
								window.location.href = "/admin/students";
							});
						},
						error: function (response) {
							swal("Student information edit failed", {
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

	// faculty
	$(".save_faculty_btn").click(function (e) {
		e.preventDefault();

		var fname = $(".faculty_fname").val();
		var lname = $(".faculty_lname").val();
		var dob = $(".faculty_dob").val();
		var email = $(".faculty_email").val();
		var address = $(".faculty_address").val();
		var contact = $(".faculty_contact").val();

		if (
			fname == "" ||
			lname == "" ||
			dob == "" ||
			email == "" ||
			address == ""
		) {
			swal("Fill up all fields", {
				icon: "error",
			});
		} else {
			swal({
				text: "Are you sure you want to add this teacher information?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			}).then((willAdd) => {
				if (willAdd) {
					$.ajax({
						type: "POST",
						url: "/admin/faculty",
						data: {
							teacher_fname: fname,
							teacher_lname: lname,
							teacher_dob: dob,
							teacher_email: email,
							teacher_address: address,
							teacher_contact: contact,
						},
						success: function (response) {
							swal("Teacher information edited successfully", {
								icon: "success",
							}).then((result) => {
								location.reload();
							});
						},
						error: function (response) {
							swal("Teacher information add failed", {
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

	$(".archive_teacher_btn").click(function (e) {
		e.preventDefault();

		var teacher_id = $(".teacher_id").val();

		swal({
			title: "Are you sure?",
			text: "Once archive, this teacher information can't be restored",
			icon: "warning",
			buttons: true,
			dangerMode: true,
		}).then((willArchive) => {
			if (willArchive) {
				$.ajax({
					type: "POST",
					url: `/admin/faculty/archive/${teacher_id}`,
					success: function (response) {
						swal("Teacher information edited successfully", {
							icon: "success",
						}).then((result) => {
							location.reload();
						});
					},
					error: function (response) {
						swal("Teacher information add failed", {
							icon: "error",
						}).then((result) => {
							location.reload();
						});
					},
				});
			}
		});
	});

	// account
	$(".save_username_teacher").click(function (e) {
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
						url: "/admin/settings",
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

	$(".save_password_admin").click(function (e) {
		e.preventDefault();

		var adminCurrentPassword = $(".admin_current_password").val();
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
		} else if (adminCurrentPassword != currentPassword) {
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
						url: "/admin/settings/password",
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
