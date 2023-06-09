import os
import argparse
import numpy as np
import torch
import matplotlib.pyplot as plt
import lightning.pytorch as pl
from Unet import Unet
from torchvision import transforms
from torchvision.datasets import OxfordIIITPet
from torch.nn import functional as F
from torch.utils.data import DataLoader, random_split
from lightning.pytorch import seed_everything
from utils import compute_metrics
import torchvision.transforms.functional as TF


def main(args):
    model = Unet.load_from_checkpoint(args.model_path)
    model.eval()

    image_transform = transforms.Compose(
        [
            transforms.Resize((240, 240)),
            transforms.ToTensor(),
        ]
    )
    target_transform = transforms.Compose(
        [
            transforms.Resize((240, 240)),
            transforms.PILToTensor(),
        ]
    )
    dataset = OxfordIIITPet(
        root="../../data",
        download=True,
        target_types="segmentation",
        transform=image_transform,
        target_transform=target_transform,
    )

    output = model(dataset[93][0].unsqueeze(0))
    # output = F.softmax(output, dim=1)
    output = torch.argmax(output, dim=1)
    output = output.squeeze().detach().cpu().numpy()

    fig, ax = plt.subplots(1, 3, figsize=(10, 5))
    ax[0].imshow(dataset[93][0].permute(1, 2, 0))
    ax[1].imshow(dataset[93][1].permute(1, 2, 0))
    ax[2].imshow(output)
    plt.show()


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("--model_path", type=str, required=True, help="Path to the model")

    args = arg.parse_args()
    seed_everything(42)
    main(args)
