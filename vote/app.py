const express = require("express");
const app = express();

app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.send(`
    <h1>Vote</h1>
    <form method="POST">
      <button name="vote" value="cats">Cats</button>
      <button name="vote" value="dogs">Dogs</button>
    </form>
  `);
});

app.post("/", (req, res) => {
  console.log("Vote:", req.body.vote);
  res.redirect("/");
});

app.listen(80, () => {
  console.log("Vote app running on port 80");
});
