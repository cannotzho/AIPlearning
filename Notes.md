Notes

This file is just for me to have a space to log my thoughts about the project as I'm having them, so that I don't forget anything.

Will organize things as I go along.

BACKEND

-Create RESTful API using python web framework - need to understand what this means
according to gemini... REST has the following characteristics:

-Client-Server Architecture: The client and server are separate, allowing for independent development and scaling.

-Statelessness: Each client request to the server contains all necessary information, and the server does not store any client context between requests. > i.e. the server should be able to to respond to each request independently regardless of requests which came before?

-Cacheability: Responses can be explicitly or implicitly marked as cacheable to improve performance and network efficiency.

-Uniform Interface: This is a core principle, ensuring a standardized way for clients to interact with resources. It involves:

    -Resource Identification: Resources are identified by unique URLs.

    -Resource Manipulation through Representations: Clients interact with resources by exchanging representations (e.g., JSON, XML) of those resources. > reducing size of information that's being passed around?

    -Self-descriptive Messages: Each message contains enough information to be processed, including HTTP methods (GET, POST, PUT, DELETE) and status codes.

    -Hypermedia as the Engine of Application State (HATEOAS): Messages include links to related resources, guiding the client through the API.

-Layered System: The architecture allows for hierarchical layers (e.g., load balancers, proxies) that are transparent to the client. > will understand what this means later

-Code-on-Demand (Optional): Servers can temporarily extend or customize client functionality by transferring executable code. > interesting

What are API endpoints?
-URLs for an API client to get resources

Looks like I will have to go through a flask tutorial first to understand Python web frameworks before understanding how endpoints are defined

I'll create a folder called Examples to keep all the files I create for my own learning that's not directly related to the tasks

Finished the Flask app basic tutorial - that was pretty useful. It covered a bit of db stuff as well which is gonna be useful later

I can probably set up the skeleton of the backend for task 1a now. First thing i want to do is create the venv for this app

Seems like the main things the app is supposed to do is detect objects from submitted videos and then have a database of entries summarizing their detected objects. db entries should have the following: video file name, detected objects, frame timestamps, and created timestamp

hmm since the assignment split the tasks into backend frontend i guess i will focus on the functionality first and check by manually uploading some test videos first

    b) Implement video processing capabilities:
    * Use lightweight, CPU-friendly models for key frame selection (e.g., scene change detection using OpenCV)
    * Implement basic object detection using a lightweight model (e.g., MobileNet SSD via OpenCV's DNN module)
    * Generate text embeddings for detected objects using a lightweight embedding model (e.g., sentence-transformers/all-MiniLM-L6-v2)
    * Create a summary of detected objects and their timestamps

find out more about lightweight models - presumably key frame selection is a method to filter out any video frames which would be uninteresting?
to rephrase the broken down tasks within video processing, its:
1 - identify key frames to perform analysis
2 - object detection on an image (aka the chosen frame)
3 - generate text embeddings for objects
4 - summarize detected objects and their timestamps

no. 2 is maybe the most interesting one right now and kind of the basis of the whole video processing so i'll figure that out first

Following the example given in the task, i've looked into the mobile net model and it seems like setting up simple object deetection with a webcam feed is quite straightforward - i will attempt this first for my own learning and then see how i can apply this within the app later. As far as lightweight models go, there are quite a number to choose from but I will just choose this first. Architecturally if i want to change the model later on it should be possible by simply switching out the scripts that the endpoints are referring to. However from a preliminary look, R-CNN is definitely out of the question due to the computing requirements so it is at least narrowed down to SSD or YOLO approaches which both look at the image only once, greatly reducing the computing load

Managed to get the mobilenet SSD to work using the really simple implementation of caffe model framework, but using mobilenet SSDlite v2 from someone else's repo gave super bad accuracy. Wondering if i should move on to the next task first since trying to do the tensorflow conversion to caffe model requires a lot of nonsense and setup... another option would be to try using the open model zoo which seems quite versatile in terms of testing different models, but it also takes some effort to set up. I can always come back again once i've done the other parts.

next on the list... analyze a video file instead and do key frame selection, before object detection, get the list of detected objects n timestamps, which are just the frame numbers they were identified on. Need to find out what they mean by text embedding? -> Did some research and its the process of converting text into numerical vectors which can represent their meaning and context. But what does it mean here - generating text embedding means to create association between detected objects which are often seen together? or to use text embedding model to summarize a frame. Will take a look at the sentence transformer to learn more. 

Ok it seems like this step is mainly to setup for the search portion of the assignment. Since they gave the example of a sentence transformer model, I guess the idea is to create a sentence with the detected objects and embed this sentence? I'm not very sure what is the input that's supposed to go into the embedded space here... if let's say a video of a person dancing, a video of a dog barking and a video of a plane are in the database, a search of "plane" needs to recommend the last video, based on the detected object or the filename which hopefully has the word plane in it too. Related searches like "flying" or "jet" should also be suggesting the plane video. The pretrained model for the sentence transformer is the component which "understands" sentence meanings, so even if an unexpected search like "singapore airlines" is submitted, it will hopefully identify the plane video as the closest neighbor in the embedded space, which means the plane video needs to have a representation in embedded space which is, presumably a sentence which can be used to reference the video. What kind of sentence can summarize a list of objects and their timeframes? Is it enough to literally embed a summarized list of objects within each frame and their timestamps or do i have to prosify the textual description somewhat... or am I meant to simply take the text embeddings at face value and just embed the object names by themselves? The video will then keep a summary of detected objects and when a query is submitted it will recommend based on how frequently that object appears in the video? idk i guess i will try a few different approaches with some example videos of my own.

Sentence transformer and scene change detection implementation were super straightforward with the well made packages... thank goodness for the modern geniuses who figured all that stuff out. I want to prioritize creating a functional prototype first so I won't dwell too much on how optimized the solution is. My next steps will be to create a frankenstein of the different parts of video processing first, then once it works in concept i'll refactor the code into classes in the actual backend folder. If I want to write/clone better implementations of each step I can just create new subclasses and pass that as an argument in the main backend script that's calling on everything. Hopefully structuring things in this way works out as expected. After that I still need to figure out the frontend stuff so I'll leave the improvements to the very end.

Whaaat the shucks!! Just consulted my bro and he explained to me why my plan to embed the entire video summary was garbage. Now I know what a relational db is and why SQLite was even suggested. I guess at least this means I just need to embed detected objects as is rather than care about forming a sentence summary. Thank goodness, I nearly wasted a whole bunch of time. Actually the worst part is my original solution might actually have worked and I wouldn't be able to tell what's wrong with it due to the small database size of 3 vids.

I managed to complete the backend prototype and it works somewhat, but there's two problems: the scene detection isn't really doing what i think it does, i think it's more designed to recognize shot changes than like, new objects coming in and out of view. So I haven't really been extracting any key frames this whole time, the library was just taking out 3 frames and treating the entire video as one scene...

The second problem is that the accuracy of the model really sucks, but I feel like that's not that important right now. I need to extract the key frames. Once I do that I can refactor everything and start working in the devel branch.

SIAN i wasted so much time on the key frames tryna find a library to do it for me when comparing histograms doesn't actually require all that much. I dug through PySceneDetect Documentation for so long to get timestamp of the key frames out... Anyway it feels good to actually have the program work as expected. I should move to devel and go refactor now.

During the process of implementing the code within the proper architecture I'm facing a bit of confusion... I created a service module for the video processing functionality, but not sure if I should do the writing to DB stuff there on in routes.py. Feel like it makes more sense to have that writing functionality within the service module so that I can keep to OOP better, but also feel like it might make the processing less efficient. I'm also not sure if i should have the keyword check done during the object detection step or after i have the list of detected objects... it feels kinda bad to iterate over the generated dict again. I guess I could link all database writing functionality to the models.py so all the functions stay where they're supposed to?

bruh i spent one hour trying to retrieve values from the sqlite database. I knew the entries were being added correctly but I kept getting the sqlalchemy row object instead of the model class and failing to access the attributes by name. Turns out I just needed to use scalars() to get the row in model form. Why does the documentation say the row object behaves like a named tuple when it just doesn't seem to work or load properly??? that was rly starting to pmo zzz

Anyway after much struggling I actually got the first part of the app to work; that is, when the server is running, the client can upload videos which automatically get processed and add all the relevant information to the database in the backend. It's also possible to click into individual videos but the page doesn't display much yet. I'm thinking of using this page to show the extracted key frames per video with the highlighted parts. This means i probably will save the keyframes to another folder that I can retrieve by video filename. I think if I had more time i might have done it so that instead of saving the images, i have another table in my db which remembers all the bounding box information per frame, per video. Then I can run a service on the backend to show the frames directly from the video file with the drawn boxes. Alas, I'm too lazy to set that up rn. I might save a first frame with the same name so that I can display a thumnail of each video in the videos page tho, at least it won't look so boring.

Next i have to create a service and start working on the vector similarity search there. I haven't been using my version control v well also, it's probably time to do a bit of housekeeping on that end too urghh ><

