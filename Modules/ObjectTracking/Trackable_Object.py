

class Trackable_Object:
    def __init__(self, object_id, center, in_boundary, counting_boundary, out_boundary, mark=False):

        self.object_id = object_id
        self.center = center
        self.first_in = center

        self.counted = False
    
        self.isValid = False

        self.in_boundary = in_boundary
        self.counting_boundary = counting_boundary
        self.out_boundary = out_boundary

        self.mark = mark

        self.valid_object()

    def valid_object(self):
        self.isValid = self.in_boundary > self.first_in[0]

    def updateCenter(self, center, mark):
        ret = False
        self.mark = mark
        self.center = center
        if self.counted:
            ret = False
        elif self.out_boundary > self.center[0] > self.counting_boundary and self.isValid:
            self.counted = True
            ret = True

        return ret

    def checkObject(self):
        return self.counted