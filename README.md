# Twitter bot for image denoising

Simple twitter bot that uses an AI denoising model (RIDNet) and replies with a denoised image as output. This bot uses both available api's (v1.1 and v.1.2). The model and related functions were extracted from [this repo](https://github.com/sunilbelde/Imagedenoising-dncnn-ridnet-keras).

## Usage
1. Get your twitter account credentials from the developers platform and paste them into `credentials.py`.
2. Add your twitter account name into `main.py`
3. `docker build -t name-image .` in Dockerfile path.
4. Run the image `docker run name-image`.
5. Mention your bot in twitter with a noisy image.

[RIDNet paper reference](https://arxiv.org/abs/1904.07396)
