

class FileMixer:
    def mix2(file1Path, file2Path, outputFilePath, manipulationFunction):
        with open(file1Path, 'rb') as f:
            file1 = f.read()
        with open(file2Path, 'rb') as f:
            file2 = f.read()

        outputBytes = manipulationFunction.mix(file1, file2)

        with open(outputFilePath, 'w') as f:
            f.write(outputBytes)

    def mix1(filePath, outputFilePath, manipulationFunction):
        with open(filePath, 'rb') as f:
            file = f.read()

        outputBytes = manipulationFunction.mix(file, None)

        with open(outputFilePath, 'w') as f:
            f.write(outputBytes)
