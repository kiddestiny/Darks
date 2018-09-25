from math import hypot
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

class coord:  
    def __init__(self, lat=0, lng=0):
        self.lat = lat
        self.lng = lng
    
    def __str__(self):
        return '地图位置 经度：%s 纬度：%s' % (self.lng,self.lat)

    def __repr__(self):
        return  "%s(lat=%r, lng=%r)" % (self.__class__.__name__, self.lat, self.lng)


if __name__ =='__main__':
    c = coord(lat=31.4455, lng=121.4565555)
    print(c)