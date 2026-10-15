# Kristian Sotiri
## Computer Science Portfolio

Welcome to my professional e-portfolio. I am a software engineer with a unique background that blends technical problem solving with creative storytelling. I hold a Bachelor of Arts in Theater, Film, and Digital Production and I am currently completing my Bachelor of Science in Computer Science at Southern New Hampshire University. 

My professional experience working for The Walt Disney Company has taught me how to thrive in highly collaborative, fast-paced environments. Now, my primary focus is transitioning into a Junior Software Engineer role with the ultimate goal of becoming an AI Solutions Engineer. I am passionate about building scalable software architectures, optimizing complex algorithms, and securing database environments. 

### Informal Code Review
Below is a comprehensive video code review of two foundational academic projects. In this walkthrough, I analyze the original code structures, identify areas for improvement, and outline my strategies for upgrading them to meet professional industry standards.

<div align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/SVMmDMB4QXs?si=QaVXdQK-zHno390U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

<br>

### Artifact Enhancements
As part of my Computer Science capstone, I am currently enhancing several projects to demonstrate my technical proficiency across three core categories. These repositories will be updated as the enhancements are finalized.

**1. Software Design and Engineering**
*Project: Grazioso Salvare Animal Rescue Dashboard*

* [View Original Dashboard Code (Dash Framework)](Software-Design/Original_Dashboard.py)
* [View Original CRUD Code](Software-Design/Original_AnimalRescueCRUD.py)
* [View Enhanced UI Code (CustomTkinter)](Software-Design/AnimalRescueDashboard.py)
* [View Enhanced Backend Code (CRUD Module)](Software-Design/AnimalRescueCRUD_Enhanced.py)

**Artifact Description**
The Grazioso Salvare Animal Rescue Dashboard was originally created during my time in the CS 340 Client/Server Development course. It is a frontend interface designed to interact with a MongoDB database containing thousands of animal rescue records. The application allows users to filter dogs based on specific rescue training categories and dynamically updates a data grid, a pie chart, and a geographic location map to reflect those precise queries.

**Justification and Architectural Trade-Offs**
I selected this artifact for my e-portfolio because it provides a highly visual representation of my ability to build end-to-end software solutions. Originally, this project was built and housed entirely within a Jupyter Notebook using the web-based Dash framework. While Dash handles component reactivity automatically, web-based notebooks are notoriously difficult to test, maintain, and deploy as standalone software. 

To showcase my software engineering skills, I completely refactored the notebook into an executable desktop application using the CustomTkinter framework. I chose a desktop framework over a web framework because it allows the application to be easily packaged and distributed to end users without requiring them to run a local development server. The trade-off of this decision was that I had to manually manage the application state and event listeners, rather than relying on Dash's automated callbacks. To handle this, I redesigned the architecture to follow a strict Model-View-Controller pattern, creating a dedicated `DashboardApp` class to isolate the UI layer from the data layer. 

**Testing and Verification**
To prove that the software works correctly under failure conditions, I conducted a series of specific system tests:
* **Invalid Credentials:** I tested the system by routing an incorrect password through the `MONGO_PASS` environment variable. Instead of crashing, the CRUD module successfully caught the `OperationFailure`, logged the security error to the console, and allowed the UI to load in a safe, empty state.
* **Database Connection Failures:** I altered the `MONGO_HOST` variable to an invalid IP address. The system successfully caught the `ConnectionFailure` and halted gracefully. 
* **Missing Location Data:** I verified that selecting a database record missing latitude and longitude coordinates did not crash the map widget. By implementing a silent `pass` within a `ValueError` check, the application ignores the missing data and waits for the next user selection. 
* **User Selection Behavior:** I systematically clicked through the UI radio buttons and verified that the treeview, pie chart, and map dynamically cleared and re-rendered the correct data payload for each rescue category. 

**Course Outcome Alignment**
I successfully met the course outcome I originally planned for this enhancement. By rebuilding the application into a structured, object-oriented format and actively verifying its failure states, I demonstrated the ability to design and evaluate computing solutions using industry standard practices. I also addressed a major security vulnerability by removing the hardcoded database credentials from the script and securely routing them through operating system environment variables. 

**Reflection**
Reflecting on the enhancement process, the biggest challenge I faced was translating reactive web components into a local desktop framework. I had to figure out how to cleanly bind the selection events from the `ttk.Treeview` data table to the `tkintermapview` widget so that clicking a row would instantly drop a pin on the map. Overcoming this challenge and manually mapping the event listeners taught me a great deal about event-driven programming and how to build resilient user interfaces.

**2. Algorithms and Data Structures**
*Project: Academic Course Catalog System*

* [View Original Code (Vector and Linear Search)](Algorithms/Original_CourseLookup.cpp)
* [View Enhanced Code (AVL Tree Implementation)](Algorithms/CourseLookup_Enhanced.cpp)

**Artifact Description**
The Academic Course Catalog System is a C++ command-line application originally developed for the CS 260 Data Structures and Algorithms course. The program parses a CSV file containing course data and prerequisites, loads it into a data structure, and provides a menu-driven interface for users to print the entire catalog or search for specific courses.

**Justification and Architectural Trade-Offs**
I selected this artifact because it demonstrates my ability to optimize software performance by implementing complex, self-balancing data structures from scratch. The original application stored course objects in a standard C++ `std::vector` and utilized a linear search algorithm. While vectors have minimal memory overhead, linear searches result in $O(N)$ time complexity, which scales poorly as a database grows.

To optimize the program, I replaced the vector with a custom AVL Tree. This required manual C++ pointer management to build the nodes and implement the left and right rotation logic. The primary architectural trade-off of this decision was memory footprint; maintaining an AVL tree requires allocating extra memory per node to store left pointers, right pointers, and height integers. However, because this application is highly read-intensive, the extra memory overhead is highly preferable to guarantee an $O(\log N)$ search time. Additionally, this structure natively allows for an in-order traversal, eliminating the need to write a separate sorting algorithm to print the catalog alphabetically.

**Testing and Verification**
To ensure the integrity of the AVL tree, I conducted a series of specific behavioral tests:
* **Multiple Insertions and Balancing:** I parsed an unsorted CSV file of courses to test the tree's automatic balancing logic. I verified that the Left-Right and Right-Left rotations successfully executed after multiple insertions, maintaining a balanced tree height and preventing the structure from degrading into a linked list.
* **Successful Searches:** I queried various course IDs and verified that the tree correctly retrieved and outputted the specific course titles and associated prerequisites in logarithmic time.
* **Ordered Traversal:** I executed the "Print Course List" command and validated that the in-order traversal correctly printed the alphanumeric course IDs in perfect ascending order.
* **Duplicate Course Handling:** I tested the insertion of duplicate course IDs to verify the system's fault tolerance, ensuring the application handles redundancies gracefully without crashing or unbalancing the tree structure.

**Course Outcome Alignment**
This enhancement thoroughly demonstrates the algorithms and data structures outcome. By manually managing memory pointers and implementing a mathematically balanced tree structure, I showcased advanced algorithmic logic and the ability to evaluate the time-space complexities of different data structures to solve a specific performance bottleneck.

**Reflection**
Reflecting on this enhancement, the most significant challenge was writing the specific pointer reassignment logic for the AVL rotations. Visualizing how the root, left, and right child pointers needed to shift during a double rotation required careful diagramming to avoid memory leaks or segmentation faults. Overcoming this challenge significantly deepened my understanding of low-level memory management in C++ and how data structures operate under the hood.

**3. Databases**
*Project: MongoDB CRUD Module*

* [View Original Code (Basic Queries)](Software-Design/Original_AnimalRescueCRUD.py)
* [View Enhanced Code (Schema Validation & Aggregation)](Software-Design/AnimalRescueCRUD_Enhanced.py)

**Artifact Description**
The artifact selected for this enhancement is the AnimalRescueCRUD backend module, originally developed for the CS 340 Client/Server Development course. This Python script serves as the communication bridge between the frontend desktop application and the MongoDB database containing the Grazioso Salvare animal rescue records. It establishes the secure network connection and handles all creation, reading, updating, and deletion operations for the system.

**Justification and Enhancements**
I included this artifact in my e-portfolio because it clearly showcases my ability to manipulate databases and implement defensive programming principles. The original academic version of this module simply passed raw query dictionaries from the frontend directly into basic MongoDB read operations. To bring this up to professional standards, I completely overhauled how the database processes and protects data. 

First, I implemented strict schema validation at the database level by sending a `$jsonSchema` command directly to MongoDB. This forces the database engine to reject any incoming documents that lack required fields like animal type, breed, or age. Second, I removed the hardcoded query logic from the frontend UI and created a secure aggregation pipeline within the CRUD module. Using the `.aggregate()` function, the backend now utilizes `$match` and `$sort` stages to filter the mountain, water, and tracking rescue candidates entirely on the server side. This minimizes network payload sizes and abstracts the database architecture away from the client.

**Testing and Verification**
To prove the security and efficiency of these database enhancements, I conducted specific backend tests:
* **Schema Validation Rejections:** I attempted to insert malformed records into the database, specifically omitting the required `breed` field and passing a negative integer for the `age_upon_outcome_in_weeks`. The MongoDB server successfully intercepted and rejected these injections. The Python module caught the resulting `OperationFailure`, logged the rejection securely without crashing, and prevented the bad data from corrupting the database.
* **Aggregation Pipeline Accuracy:** I queried the database for "water" rescue candidates. The pipeline successfully executed the `$match` stage on the server, returning a precise payload containing *only* Intact Female Labradors, Golden Retrievers, and Newfoundlands between 26 and 156 weeks old. Furthermore, the `$sort` stage correctly ordered the returned records by age in ascending order, verifying that the server-side computation worked flawlessly before the data ever reached the frontend UI.

**Course Outcome Alignment**
This enhancement directly meets the course outcomes for both database management and software security. As my instructor noted during the code review, simple Python validation is not enough to stop malicious injections. By implementing true schema validation on the database itself alongside secure credential routing via environment variables, I successfully demonstrated the security outcome of mitigating structural design flaws. Furthermore, constructing the aggregation pipeline proves my capability to optimize complex database queries and manage large data structures efficiently.

**Reflection**
The process of enhancing this database module highlighted the critical difference between writing code that works and writing code that is secure. The biggest challenge I faced was configuring the schema validation rules using the `collMod` command. If the rules were too strict, legitimate rescue records were rejected. If they were too loose, it defeated the purpose of the security enhancement. I had to carefully map out the exact BSON data types expected by the database and wrap the validation command in a dedicated try and except block to gracefully handle permission boundaries. Overcoming this hurdle taught me how to securely design backend architectures that do not rely blindly on the frontend interface to provide clean data.

---

### Connect With Me
Thank you for taking the time to review my portfolio. Feel free to explore my GitHub repositories to view the source code for these projects.
