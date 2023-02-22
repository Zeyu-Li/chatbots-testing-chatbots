import { test, expect } from '@playwright/test';
import * as fs from 'fs';

// Load the contents of the file into a string variable
const fileContents: string = fs.readFileSync('test.txt', 'utf-8');

// Split the string into an array of strings using the newline character
const sentences: string[] = fileContents.split(/\r?\n/);

function delay(time) {
  return new Promise(function(resolve) { 
      setTimeout(resolve, time)
  });
}

const mockWait = async () => {
  // add some random delay in seconds plus or minus
  const delayTime = Math.floor(Math.random() * 1000) * 90;
  const baseDelay = 250000;

  const isPositive = Math.random() >= 0.5;
  await delay(delayTime + (isPositive ? baseDelay : -baseDelay));
}

test('Mock testing', async ({ page }) => {
  await page.goto('https://accounts.google.com/');

  // login
  await page.fill('input[type="email"]', process.env.GOOGLE_EMAIL!);
  await page.click('div#identifierNext');
  await page.fill('input[type="password"]', process.env.GOOGLE_PASSWORD!);
  await page.click('div#passwordNext');

  // wait for login to complete and has Welcome in h1
  await page.waitForSelector('h1:has-text("Welcome")');

  await delay(1000);

  await page.goto('https://www.google.com/bard');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Bard/);

  // store time for later
  const startTime = new Date().getTime();
  const endMinTime = 61;
  let index = 0;

  // while 61 minutes have not passed
  while (new Date().getTime() - startTime < endMinTime * 60 * 1000) {
    // if we have reached the end of the sentences, start over
    if (index >= sentences.length) {
      index = 0;
    }
    
    // input sentence[i] into the textarea
    await page.fill('textarea', sentences[index]);

    // enter button
    await page.keyboard.press('Enter');

    // wait for the response
    await mockWait();
    
    index++;
  }
});