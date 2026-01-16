After I graduated University, I have realised that many things that I am signed up for (credit cards, memberships, phone contracts, work benefits etc) have a wide range of perks that I am unaware of, that could have saved me a lot of money.

One example is that my work perk program offers discounts on AirBnB stays, but I only found out about it after I was snooping around on my benefits page.
Having booked multiple holidays since I had found this, this could have saved me hundreds of pounds in the long run. Having then snooped further, I saw other things such as supermarket discounts which would have been really useful when doing large online shops, or airline discounts where a certain airline would give a few percentage off through my American Express discount scheme.

The point of this application is to collate all of these perks in one place, so that I can easily see what discounts they are eligible for based on the various things I am signed up for. This will be as automated as possible, but there will be heavy restrictions.

<h4>The service that I would like to extract may not have an API, or may have restrictions on the type of requests that can be made (requiring human like behaviour). </h4>

So there are three ways I will be approaching this to streamline my experience as much as possible:
1. Where there is no API and on mobile application only (Monzo for example), I will be uploading screenshots of the perks page, and using OCR alongside AI to extract the relevant information. I will need to investigate how much of this I can automate.
2. Where there is a web application, I will be using web scraping techniques to extract the relevant information. I will need to see how best to emulate 'human like behaviour' to avoid being blocked by anti-bot measures. - If this fails, then a manual login may be required and then I will be able to extract the HTML if there is no API required.
3. Where there is an API, I will be using this to extract the relevant information.

The technical architecture will focus on being as modular and as possible, so that I can easily add new services (plug and play) as I sign up for them.

The end goal of this application is to have a dashboard where I can see all of my perks in one place, with links to the relevant pages so that I can easily access them when needed. This will save me time and money in the long run, and will help me to make the most of the various services that I am signed up for.

