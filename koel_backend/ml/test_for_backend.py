audio_file = request.FILES.getlist('audio')  # This is an instance of MIME (in-memory object)
        # audio_file = request.FILES['audio']

try:
    # Save audio file temporarily
    file_names = []
    if audio_file:
        for file in audio_file:
            temp_file_path = os.path.join(os.getcwd(), '\\tmp', file.name)
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            file_names.append(temp_file_path)
            with open(temp_file_path, 'wb') as f:
                f.write(file.read())