const navControl = (navbar, open, close) => {
	const nav = document.querySelector(`.${navbar}`);
	const openBtn = document.querySelector(`.${open}`);
	const closeBtn = document.querySelector(`.${close}`);

	openBtn?.addEventListener("click", () => {
		nav.style.display = "flex";
		openBtn.style.display = "none";
		closeBtn.style.display = "block";
	});

	closeBtn?.addEventListener("click", () => {
		nav.style.display = "none";
		openBtn.style.display = "block";
		closeBtn.style.display = "none";
	});
};

navControl("nav-teacher-links", "teacher-open-btn", "teacher-close-btn");
navControl("nav-parent-links", "parent-open-btn", "parent-close-btn");
