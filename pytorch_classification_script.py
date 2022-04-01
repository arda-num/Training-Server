import os
import torch
import torch.utils.data
# import torchvision
from PIL import Image
import cv2
from pycocotools.coco import COCO



class cocoDataset(torch.utils.data.Dataset):
    def __init__(self, root, annotation, transforms=None):
        self.root = root
        self.transforms = transforms
        self.coco = COCO(annotation)
        self.ids = list(sorted(self.coco.imgs.keys()))

    def __getitem__(self, index):
        # Own coco file
        coco = self.coco
        # Image ID
        img_id = self.ids[index]
        # List: get annotation id from coco
        ann_ids = coco.getAnnIds(imgIds=img_id)
        # Dictionary: target coco_annotation file for an image
        coco_annotation = coco.loadAnns(ann_ids)
        # path for input image
        path = coco.loadImgs(img_id)[0]['file_name']
        # open the input image
        # img = Image.open(os.path.join(self.root, path))
        img = cv2.imread(os.path.join(self.root, path))
        # Labels 
        label = coco_annotation[0]["category_id"]
        label = torch.tensor(label)
        # Tensorise img_id
        img_id = torch.tensor([img_id])
    
        # Annotation is in dictionary format
        my_annotation = {}
        my_annotation["label"] = label
        my_annotation["image_id"] = img_id

        if self.transforms is not None:
            img = self.transforms(img)

        return img, my_annotation

    def __len__(self):
        return len(self.ids)



def train(clientID):
    current_path = os.getcwd()
    train_data_dir = os.path.join(current_path,"train_data",clientID,"images")
    train_coco = os.path.join(current_path,"train_data",clientID,"coco","annotations.json")
    # path to your own data and coco file


    # create own Dataset
    dataset = cocoDataset(root=train_data_dir,
                            annotation=train_coco,
                            #   transforms=get_transform()
                            )

    # collate_fn needs for batch
    def collate_fn(batch):
        return tuple(zip(*batch))


    # Batch size
    train_batch_size = 1

    # own DataLoader
    # data_loader = torch.utils.data.DataLoader(dataset,
    #                                         batch_size=train_batch_size,
    #                                         shuffle=True,
    #                                         num_workers=4,
    #                                         collate_fn=collate_fn)

    train_length=int(0.8* len(dataset))

    test_length=len(dataset)-train_length

    train_dataset,test_dataset=torch.utils.data.random_split(dataset,(train_length,test_length))

    dataloader_train=torch.utils.data.DataLoader(train_dataset,
                                            batch_size=train_batch_size,
                                            shuffle=True,
                                            collate_fn=collate_fn)

    # select device (whether GPU or CPU)
    # device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    device = torch.device("cpu")


    # DataLoader is iterable over Dataset
    returnArr = list()
    for imgs, annotations in dataloader_train:  # imgs are lists of images which has length of train_batch_size
        for img in imgs:
            returnArr.append(img)
    return returnArr


# cv2.waitKey(0)


# number_of_labels = 10

# model = torch.hub.load('pytorch/vision', 'mobilenet_v2', pretrained=True)

# model.classifier[1] = torch.nn.Linear(in_features=model.classifier[1].in_features, out_features=number_of_labels)
# print(model.classifier)

# # model.classifier[1] = nn.Linear(1280, 10)


# with torch.no_grad():
#     pass
#     #make prediction here
#     # y_predicted = model(X_test)


