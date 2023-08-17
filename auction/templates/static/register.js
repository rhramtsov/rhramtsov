let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
fetch("/your-endpoint/", {
  method: "POST",
  headers: {
    "X-CSRFToken": csrftoken
  },
  body: JSON.stringify(data)
});
