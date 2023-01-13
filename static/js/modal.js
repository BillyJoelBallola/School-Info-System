const modal = document.querySelector(".modal");
const modalClose = document.querySelector(".btn-close");
const modalAdd = document.querySelector(".btn-add");

modalClose?.addEventListener("click", () => {
	if (modal.classList.contains("show")) {
		modal.classList.remove("show");
	}
});

modalAdd?.addEventListener("click", () => {
	if (!modal.classList.contains("show")) {
		modal.classList.add("show");
	}
});
