Tasks:
•	Fix so the design of the images is like the attached picture in the root folder (preview.jpg)
•	Implement so you can click on the Share link and retrieve a full page that is SEO friendly
•	Style the share link so that it looks like the button in the preview
•	Add some kind of status when the AJAX is running, something like "Requesting, Retrieving"
•	Display whatever the pictures are retrieved from the cache or not, like "Loaded from cache / Loaded from flickr"
•	Implement so the cache helper (CacheHelper.cs) has support for both reference types and value types
•	In HomeController, add a feature so you can select between FlickrCacheableRepository or FlickrRepository by some configuration flag, create a solution that are easy to extend so you can have N numbers of repositories
•	Change HomeController's GetImage method only to allow POST request, update the JavaScript so the functionality still work
•	New images should fade in when they are added to the DOM, focus only on the image so each of the images loads smoothly and are display ready.
•	Style the application to look like the attached preview (background image found in the root of the Demo folder)
•	Create a responsive layout so that the application looks good in all resolutions (1 image per row in mobile, 5 on tablet and 10 on high resolution computers)
