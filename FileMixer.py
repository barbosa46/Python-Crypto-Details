

class FileMixer:
    def mix2(file1Path, file2Path, outputFilePath, manipulationFunction):
        with open(file1Path, 'r') as f:
            file1 = f.read()
        with open(file2Path, 'r') as f:
            file2 = f.read()

        outputBytes = manipulationFunction.mix(file1, file2)

        writemode = "wb"
        if isinstance(outputBytes, str):
            writemode="w"

        with open(outputFilePath, writemode) as f:
            f.write(outputBytes)

    def mix1(filePath, outputFilePath, manipulationFunction):
        with open(filePath, 'r') as f:
            file = f.read()
        print(file)
        print(type(file))
        outputBytes = manipulationFunction.mix(file, None)
        print(type(outputBytes))
        print(outputBytes)

        writemode = "wb"
        if isinstance(outputBytes, str):
            writemode = "w"

        with open(outputFilePath, writemode) as f:
            f.write(outputBytes)
