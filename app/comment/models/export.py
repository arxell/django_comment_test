import pickle

from django.db import models


class Export(models.Model):

    user_id = models.IntegerField()

    data = models.BinaryField()

    def set_data(self, data):
        self.data = pickle.dumps(data)

    def get_data(self):
        try:
            return pickle.loads(self.data)
        except Exception:
            return None

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.id)
