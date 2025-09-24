# HTX Enterprise AI Products Technical Test – Software Engineer (Video Detection & Summarization)

The purpose of this test is to assess if you have the prerequisite technical ability for the role.

Please follow closely to the Test Instructions:
* You can make assumptions to any information not specified within the Test Instructions.
* You can make references to any other technical literature as required.
* Reach out to us if you have any queries via email.
* Submit Deliverables to the sender of this test.
  * The deliverable for this assignment is a link to your codebase (publicly accessible) for your attempt on the assignment.
  * All submitted artifacts must be executable without errors. If a Python environment setup is required, please include the setup scripts in the submission. Failure to comply will result in the submission being considered incomplete.
  * You have a total of 7 calendar days to complete the list of tasks (1 to 5) below by yourself, upon receiving the email.
  * You will need to document and comment your code properly and state any assumptions made within each task.

## Tasks

1. Create a public git repository e.g., https://github.com/fred/myrepo. You may use any of the publicly available repositories like GitHub, GitLab, etc.

2. Create a directory called backend in your repository for all backend-related code.

    a) Implement a RESTful API using a Python web framework (e.g., Flask, FastAPI) with the following endpoints:
    * GET /health: Returns the status of the service.
    * POST /process: Accepts video files, performs key frame extraction, object detection, and saves results in database.
    * GET /videos: Retrieves all processed videos from the database.
    * GET /search: Performs a full-text search on video summaries based on detected objects or video file name.
    (You are given 3 sample video files to use for this assignment)

    b) Implement video processing capabilities:
    * Use lightweight, CPU-friendly models for key frame selection (e.g., scene change detection using OpenCV)
    * Implement basic object detection using a lightweight model (e.g., MobileNet SSD via OpenCV's DNN module)
    * Generate text embeddings for detected objects using a lightweight embedding model (e.g., sentence-transformers/all-MiniLM-L6-v2)
    * Create a summary of detected objects and their timestamps

    c) Search Feature:
    * Use SQLite as the primary database for storing the video file name, detected objects, frame timestamps, and created timestamp.
    * For vector similarity search, implement one of the following approaches:
      * Option 1: Integrate an in-memory FAISS index that loads embeddings from SQLite on service startup
      * Option 2: Implement a lightweight vector search using a Python library such as scikit-learn's NearestNeighbors
      * Option 3: Store embeddings as serialized binary blobs in SQLite and implement cosine similarity in Python

    d) Containerisation (Ensure container configuration is optimised for CPU usage)

3. Create a directory called frontend in your repository for all frontend-related code.

    a) Develop a single-page application using a modern JavaScript framework (e.g., React, Vue.js, Angular).

    b) Implement the following features:
    * File upload interface for single/batched video file processing.
    * Display a list of all processed videos from the database.
    * Show extracted key frames with detected objects highlighted.
    * Implement search functionality to search for videos based on:
      * Text queries (matching against object labels and video filenames)
      * Visual similarity (by selecting an existing video/frame as reference)

    c) Containerisation

4. Testing

    a) Write three unit tests for the backend and frontend each. Include instructions on how to run the tests in the README.
    * Backend tests should include testing the frame extraction logic, object detection accuracy, and API endpoints.
    * Frontend tests should cover the upload functionality, search feature, and video result display.

5. Based on the full-stack application you developed, create an architecture diagram that outlines the following components:
    a) Frontend,
    b) Backend,
    c) Database and Vector Search Solution,
    d) Video Processing Pipeline,
    e) External Services, if any.

    Your answer can be saved as architecture.pdf under the main repository. Please explain your diagram, citing assumptions and considerations, particularly addressing:
    * Your chosen approach for implementing vector similarity search
    * How your solution handles larger video files
    * Potential areas for improvement with more computational resources

## Additional Notes for Candidates

1. **Frame Selection Strategy**: You're expected to implement a simple but effective approach to extract meaningful frames from videos. Consider using techniques like scene change detection, regular interval sampling, or motion analysis to identify key frames.

2. **Resource Constraints**: Your solution should work efficiently on a standard machine with/without dedicated GPU. Consider:
   * Downsampling video resolution before processing
   * Processing a limited number of frames
   * Using quantized or lightweight models

3. **Vector Search Implementation**: Document your chosen approach for implementing vector similarity search, explaining the tradeoffs between memory usage, search speed, and implementation complexity.

4. **Evaluation**: Your solution will be evaluated based on:
   * Code quality and organisation
   * Execution speed on standard hardware
   * Accuracy of object detection and summarisation
   * User experience of the frontend application
   * Thoughtfulness in architecture design given the constraints