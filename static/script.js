document.addEventListener("DOMContentLoaded", function () {

    /*
     * ==========================
     * MOBILE NAVIGATION
     * ==========================
     */

    const menuButton =
        document.getElementById("menuButton");

    const mobileMenu =
        document.getElementById("mobileMenu");

    if (menuButton && mobileMenu) {

        menuButton.addEventListener("click", function () {

            mobileMenu.classList.toggle("hidden");

        });

    }


    /*
     * ==========================
     * CHARACTER COUNTER
     * ==========================
     */

    const content =
        document.getElementById("content");

    const characterCount =
        document.getElementById("characterCount");

    if (content && characterCount) {

        function updateCharacterCount() {

            const count = content.value.length;

            characterCount.textContent =
                count + " characters";

        }

        content.addEventListener(
            "input",
            updateCharacterCount
        );

        updateCharacterCount();

    }


    /*
     * ==========================
     * FLASH NOTIFICATIONS
     * ==========================
     */

    const notifications =
        document.querySelectorAll(".flash-message");

    notifications.forEach(function (notification) {

        setTimeout(function () {

            notification.style.opacity = "0";

            notification.style.transform =
                "translateY(-10px)";

            setTimeout(function () {

                notification.remove();

            }, 300);

        }, 4000);

    });

});
/*
 * ==========================
 * DELETE MODAL
 * ==========================
 */

function openDeleteModal(articleId, articleTitle) {

    const modal =
        document.getElementById("deleteModal");

    const title =
        document.getElementById("deleteArticleTitle");

    const form =
        document.getElementById("deleteForm");


    title.textContent = articleTitle;

    form.action = "/delete-article/" + articleId;


    modal.classList.remove("hidden");

    modal.classList.add("flex");
}


function closeDeleteModal() {

    const modal =
        document.getElementById("deleteModal");

    modal.classList.remove("flex");

    modal.classList.add("hidden");

}
document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        closeDeleteModal();

    }

});