import os
from PIL import Image

class Camouflage():

  image_name = None
  image_path = None
  image = None
  pixels = None
  size = None
  average_colors = None
  color_range = None

  def __init__(self, imageName, colorRange=100):
    self.image_name = imageName
    project_dir = os.path.dirname(os.path.abspath(__file__))
    self.image_path = os.path.join(project_dir, "images", imageName)
    self.color_range = colorRange
    self.loadImage()
    self.calculateAverage()
    self.checkDifference()
    self.saveMaskedImage()

  def loadImage(self):
    self.image = Image.open(self.image_path)
    self.pixels = self.image.load()
    self.size = self.image.size
  
  def calculateAverage(self):
    total = {"r": 0, "g": 0, "b":0}
    for x in range(self.size[0]):
      for y in range(self.size[1]):
        total = {
          "r": total["r"] + self.pixels[x, y][0],
          "g": total["g"] + self.pixels[x, y][1],
          "b": total["b"] + self.pixels[x, y][2]
        }
    total_pixel = self.size[0] * self.size[1]
    average = {
      "r": int(total["r"] / total_pixel),
      "g": int(total["g"] / total_pixel),
      "b": int(total["b"] / total_pixel),
    }
    self.average_colors = average

  def checkDifference(self):
    for x in range(self.size[0]):
      for y in range(self.size[1]):
        difference = {
          "r": abs(self.pixels[x, y][0] - self.average_colors["r"]),
          "g": abs(self.pixels[x, y][1] - self.average_colors["g"]),
          "b": abs(self.pixels[x, y][2] - self.average_colors["b"])
        }
        total_difference = difference["r"] + difference["g"] + difference["b"]
        if total_difference > self.color_range:
          self.pixels[x, y] = (self.average_colors["r"], self.average_colors["g"], self.average_colors["b"])

  def saveMaskedImage(self):
    masked_image_name = "masked-" + self.image_name
    project_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(project_dir, "images", masked_image_name)
    self.image.save(save_path)

if(__name__ == "__main__"):
  Camouflage("desert.jpg", 120)
  Camouflage("moon.jpg", 50)
  Camouflage("snow.jpg", 120)
  Camouflage("flower.jpg", 100)
  Camouflage("underwater.jpg", 130)
  