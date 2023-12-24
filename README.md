# Google Cloud Generative AI API for OOP Eepow Chat Bot

## Introduction

### About OOP Eepow Chat Bot project

You can find the detailed description and source code for web application here: https://github.com/Chirox03/chat-bot-eepow

### About this API
//todo

## How to deploy the API
//todo

## How to call API

I have deployed my code to API endpoint which is used for OOP Eepow Chat Bot project.

* API endpoint to get response: https://eepow-chatbot-2023-phlyzwu6ga-uc.a.run.app/predict
* The input question should be submitted via HTTP request, using POST method in above endpoint sending a stringfied JSON in the following format `{“text”: text}`
* The returned reponse will be a string in markdown format

**Example: Calling API via ajax**: 
```
    $.ajax({
      url: 'https://eepow-chatbot-2023-phlyzwu6ga-uc.a.run.app/predict',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({"text": question}),
      success: function(response) {
        //do something with response
      }
    });
```
