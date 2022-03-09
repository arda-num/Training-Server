# Training-Server
This is a AI Model training and store server made by FAST API.

# Example
http get request example in browser to train and store:
http://127.0.0.1:8000/progress?image_count=1&train_type=classification&bucket_name=s3blob-anticode

Important: bucket_name represents user specific bucket name on the cloud

# File Organization

-- root (dir) 

    -- main.py (file)

    -- train_data (dir)

        -- user_bucket_id0 (dir)

            -- images (files...)

        -- user_bucket_id1 (dir)

            -- images (files...)

This represents a general idea of how documentation is done. When a new user requests for a training new directory added for that user. On the other hand, when an existing user requests, his/her directory is deleted and generated from scratch.


        




