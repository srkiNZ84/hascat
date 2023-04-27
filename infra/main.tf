terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}


resource "random_pet" "hostname" {
}

resource "aws_s3_bucket" "cat-image-bucket" {
  bucket = "cat-image-bucket"

  tags = {
    Name        = "Potential Cat picture bucket ${random_pet.hostname.id}"
  }
}
