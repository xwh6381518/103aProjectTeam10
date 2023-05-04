// Barry Wen

// Route for money converter
const express = require("express");
const router = express.Router();
const GPT = require("../models/gpt");
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

// render currency convert page
router.get("/money", isLoggedIn, async (req, res, next) => {
  const gptItems = await GPT.find({ userId: req.user._id });
  res.render("money", { user: req.user, gptItems });
});

// post currency convert query
router.post("/money", async (req, res) => {
  try {
    const { first, second } = req.body;
    const amount = parseFloat(req.body.amount);
    let prompt = `Please help me convert ${amount} ${first} to ${second}`;
    console.log("prompt=", prompt);
    const response = await openai.createCompletion({
      model: "text-davinci-003",
      prompt: `${prompt}`,
      max_tokens: 1024,
      temperature: 0.5,
      n: 1,
      stop: null,
    });
    let gptItem = new GPT({
      prompt: prompt,
      answer: response.data.choices[0].text,
      userId: req.user._id,
    });
    await gptItem.save();
    return res.render("moneyResponse", {
      answer: response.data.choices[0].text,
    });
  } catch (error) {
    return res.status(400).json({
      success: false,
      error: error.response
        ? error.response.data
        : "There was an issue on the server",
    });
  }
});

// remove a gpt query
router.get("/money/remove/:gptId", isLoggedIn, async (req, res) => {
  await GPT.deleteOne({ _id: req.params.gptId });
  res.redirect("/money");
});

module.exports = router;
