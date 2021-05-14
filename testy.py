from multicolorcaptcha import CaptchaGenerator

for a in range(0, 1000):
    print(f"Generowanie: {a}")
    # Captcha image size number (2 -> 640x360)
    CAPCTHA_SIZE_NUM = 20

    # Create Captcha Generator object of specified size
    generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

    # Generate a captcha image
    captcha = generator.gen_captcha_image(difficult_level=4)
    # Get information
    image = captcha["image"]
    characters = captcha["characters"]

    # Save the image to a file
    image.save(f"W:\discordtest/captcha/{a}.png", "png")