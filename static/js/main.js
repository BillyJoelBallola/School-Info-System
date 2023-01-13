let announcements = document.querySelectorAll(".announcement-p");
let articles = document.querySelectorAll(".article-content");
let events = document.querySelectorAll(".event-content");
let articleContent = document.querySelectorAll(".table-content");

const truncate = (string, n) => {
	return string?.length > n ? string.substr(0, n - 1) + "..." : string;
};

// edit selection
const selected = (value, options) => {
	const selectOption = document.querySelectorAll(options);
	const grade_value = document.querySelector(value)?.value;

	selectOption.forEach((option) => {
		if (grade_value === option.value) {
			option.setAttribute("selected", "True");
		}
	});
};

selected(".grade_value", ".grade_option");
selected(".section_value", ".section_option");

articleContent?.forEach((td) => {
	td.textContent = truncate(td.textContent, 100);
});

announcements?.forEach((announcement) => {
	announcement.textContent = truncate(announcement.textContent, 100);
});

articles?.forEach((article) => {
	article.textContent = truncate(article.textContent, 200);
});

events?.forEach((event) => {
	event.textContent = truncate(event.textContent, 500);
});
