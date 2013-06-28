import pyStage
import unittest
import shutil
import os

TESTING_FILES_PATH = os.path.join(os.path.dirname(__file__),"files")

def removeDir(folder_path):
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            removeDir(file_object_path)
            os.rmdir(file_object_path)

class TestPyStageFunctions(unittest.TestCase):

    def setUp(self):
        src = os.path.join(TESTING_FILES_PATH,"operations.json")
        print src
        dest = os.path.join(os.path.dirname(__file__),"operations.json")
        print dest
        shutil.copy(src,dest)
        self.operationsFile = dest

    def test(self):
        pyStage.checkingOperationFile(self.operationsFile)
        data = pyStage.loadingOperations(self.operationsFile)
        pyStage.checkingOperations(data)
        pyStage.creatingDestinationRootDirectory(data["destination_root"])
        pyStage.performingOperations(data["source_root"], data["destination_root"], data["operations"])
        removeDir(data["destination_root"])
        os.rmdir(data["destination_root"])

    def tearDown(self):
        os.remove(os.path.join(os.path.dirname(__file__),"operations.json"))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPyStageFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)