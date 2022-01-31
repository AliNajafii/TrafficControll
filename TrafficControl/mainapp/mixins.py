class InfoDataExtractorMixin:
    """
    This class helps Serializers to 
    Extract info data with valid
    names .
    """
    valid_names = []

    def extract_info(self,data):
        """
        this method gives dictionary of
        data and pops the valid name data
        from it and returns it.
        """
        for name in self.valid_names:
            info = data.get(name)
            if info:
                return data.pop(name)

class CarInfoDataExtractorMixin(InfoDataExtractorMixin):
    valid_names = ['ownerCar','car_set','cars']


            

