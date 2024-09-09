//Перемикач хедера для зареєстрованих користувачів
document.addEventListener("DOMContentLoaded", () => {
  const isLoggedIn = localStorage.getItem("loggedIn");

  const loggedInHeader = document.querySelector(".global__header__loggedIn");
  const loggedOutHeader = document.querySelector(".global__header__loggedOut");

  if (isLoggedIn === "true") {
    loggedInHeader.style.display = "block";
    loggedOutHeader.style.display = "none";
  } else {
    loggedInHeader.style.display = "none";
    loggedOutHeader.style.display = "block";
  }

  document.querySelector("#login-btn")?.addEventListener("click", () => {
    localStorage.setItem("loggedIn", "true");
    window.location.reload();
  });

  document.querySelector("#logout-btn")?.addEventListener("click", () => {
    localStorage.removeItem("loggedIn");
    window.location.reload();
  });
});

//Перемикач-мигалка для титулки
const title = document.querySelector(".fs-4");
const toggler = () => {
  title.classList.toggle("highlight");
};
setInterval(toggler, 1000);

//Перемикач для зміни паролю
const NewFiled = [
  `<div class="profile__change-password-container">
  <div class="form-floating mb-3">
    <input
      type="password"
      class="form-control"
      id="floatingOldPassword"
      placeholder="Old Password"
    />
    <label for="floatingInput">Old password</label>
  </div>
  <div class="form-floating">
    <input
      type="password"
      class="form-control"
      id="floatingNewPassword"
      placeholder="New password"
    />
    <label for="floatingPassword">New password</label>
    <div class="change-passsword-btn-container">
      <a class="btn btn-secondary" href="/change-password" id="change-btn"
        >Change
      </a>
    </div>
    <div class="return-btn-container">
      <a class="btn btn-danger" id="return-btn">Return</a>
    </div>
  </div>
</div>`,
];
const profileContainer = document.querySelector(".profile__container-forChangingPassword");
const changePasswordBtn = document.getElementById("change-password-btn");
const addContainer = () => {
  changePasswordBtn.style.display = "none";
  profileContainer.innerHTML += NewFiled;
  const returnBtn = document.getElementById("return-btn")
  returnBtn.addEventListener("click",removeContainer)
};
const removeContainer = () => {
  changePasswordBtn.style.display = "block";
  profileContainer.innerHTML ="";
};
changePasswordBtn.addEventListener("click", addContainer);

