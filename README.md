## TimeCapsule Project

A Django-based web application that allows users to create digital time capsules by uploading documents, videos, and other content. Users can lock their capsules, set opening dates, and share their capsules with others. The platform also enables subscription and following features, allowing users to be notified when a capsule opens.

### Features

- **User Authentication**: Secure login and registration using Django's built-in authentication system.
- **Capsule Creation**: Upload and store various types of content (documents, videos, etc.) within a time capsule.
- **Search and Discover**: Easily search for public capsules and discover new content.
- **Subscription and Following**: Follow and subscribe to capsules to receive notifications upon their opening.
- **Time Lock**: Set a future date for the capsule to be opened, mimicking the real-time capsule experience.

### Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/shashankkannan/time_capsule.git
   cd timecapsule
   ```

2. **Set Up the Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Database Setup**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server**:
   ```
   python manage.py runserver
   ```

### Usage

1. **Register and Login**: Create an account or log in with existing credentials.
2. **Create a Capsule**: Use the capsule creation form to upload files and set the opening date.
3. **Search and Explore**: Use the search bar to find public capsules.
4. **Subscribe and Follow**: Follow capsules to receive updates when they open.

