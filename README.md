# Training-Server
This is a AI Model training and store server made by FAST API.

# Example
http get request example in browser to train and store:
```ruby
http://127.0.0.1:8000/progress?train_type=classification&bucket_name=client0
```
Important: bucket_name represents user specific bucket name on the cloud

# File Organization in Local
```
root (dir) 
    main.py (file)
    train_data (dir)
        client0 (dir)
            coco (dir) 
                annotations.json
            images (dir)
                images...
        client1 (dir)
            coco (dir)
                annotations.json
            images (dir)
                images...
    weights (dir)
        client0 (dir)
            model.h5 (file)
        client1 (dir)
            model.h5 (file)
```
This represents a general idea of how documentation is done. When a new user requests for a training new directory added for that user. On the other hand, when an existing user requests, his/her directory is deleted and generated from scratch. Also notice that models are just appear before the upload operation. After the upload is done, models are deleted from local.


# Sample annotations.json file (COCO) for Classification:

```ruby
{
    "info" : {},
    "licences" : [],
    "categories" : [
        {
            "id" : 1,
            "name" : "cat"
        }
    ],
    "images" : [
        {
            "id" : 0,
            "licence" : 1,
            "file_name" : "00000001.jpg",
            "height" : 324,
            "width" : 765
        }
    ],
    "annotations" : [
        {
            "id" : 3,
            "image_id" : 0,
            "category_id" : 1,
        }
    ]
}
```

- annotations.json file must be like the above sample; otherwise, server will give an error.

# File and Bucket Organization in S3
```
root
    training-server-client0 (Bucket)
        coco (dir)
            annotations.json
        images (dir)
            images...
    training-server-client1 (Bucket)
        coco (dir)  
            annotations.json
        images (dir)
            images...
                .
                .
                .
    training-server-model-client0 (Bucket)
        model.h5 (file)
    training-server-model-client1 (Bucket)
        model.h5 (file)
            .
            .
            .
```

