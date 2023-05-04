const express = require("express");
const router = express.Router();
const TEMP = require("../models/temp");
const User = require("../models/User");
const mongoose = require("mongoose");
const { Configuration, OpenAIApi } = require("openai");

// Configuration
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

isLoggedIn = (req, res, next) => {
  if (res.locals.loggedIn) {
    next();
  } else {
    res.redirect("/login");
  }
};

router.get("/temp", isLoggedIn, async (req, res, next) => {
  const tempItems = await TEMP.find({ userId: req.user._id });
  res.render("temp", { user: req.user, tempItems });
});

// add a new temp query
router.post("/temp", async (req, res) => {
  try {
    let prompt = "Get current temperature for" + JSON.stringify(req.body) + "in F and C.";
    const response = await openai.createCompletion({
      model: "text-davinci-003",
      prompt: `${prompt}`,
      max_tokens: 1024,
      temperature: 0.5,
      n: 1,
      stop: null,
    });
    let tempItem = new TEMP({
      prompt: "Get current temperature for " + JSON.stringify(req.body) +" in F and C.",
      answer: response.data.choices[0].text,
      userId: req.user._id,
    });
    await tempItem.save();
    return res.render("tempResponse", { answer: response.data.choices[0].text});
  } catch (error) {
    return res.status(400).json({
      success: false,
      error: error.response
        ? error.response.data
        : "There was an issue on the server",
    });
  }
});

// remove a temp query
router.get("/temp/remove/:tempId", isLoggedIn, async (req, res) => {
  await TEMP.deleteOne({ _id: req.params.tempId });
  res.redirect("/temp");
});

module.exports = router;
