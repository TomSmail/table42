class PromptStorage():
    """
    This class is used to store the prompts for the prompt generation, 
    technically it stores the content though, which can include images.
    """

    def get(self, prompt_type="image_1", time_range=None, encoded_image=None, incorrect_button_labels=None, html_content=None):
        def html_1():
            return [
                {
                    "type": "text",
                    "text": '''
                        You are an expert web scraper and have been asked to extract
                        the next button or available reservation times from the following
                        HTML content. The output should be in the format:
                        { "available_times": [time1, time2], 
                            "next_button": null 
                        } or
                        { "available_times": null,
                           "next_button": <button_text> 
                        }. 
                        
                        '''
                        + f''' 
                        The user is looking for a time between 
                        {time_range.get_start()} and {time_range.get_end()}
                        Do NOT include any other information in the output.
                        Do NOT Include ```json``` in the output. 
                        Here is an example of what should be output: 
                        ''' + f'''
                        {
                        """
                            These buttons have been tried and are NOT the 
                            correct next_button, do not return them as an answer: 
                        """ + str(incorrect_button_labels) if incorrect_button_labels else ""}
                        ''' + '''
                        {
                        "available_times": null,
                        "next_button": "BOOK A TABLE"
                        } 
                        Here is the HTML content:
                        ''' + html_content
                }
            ]
        def image_1():
            return [
                {
                    "type": "text",
                    "text": '''
                        Analyze the following image and provide the
                        available reservation times or the next button to 
                        click to reach the reservation page. The output
                        should be in the format: 
                        { "available_times": [time1, time2], 
                            "next_button": null } 
                        or 
                        { "available_times": null,
                            "next_button": <button_text> }.
                        If there are no available times and no next button,
                        return 
                        { "available_times": null,
                            "next_button": null } 
                        ''' + f'''
                        The user is looking for a time between 
                        {time_range.get_start()} and {time_range.get_end()}
                        Do NOT include any other information in the output.
                        Do NOT Include ```json``` in the output. 
                        Here is an example of what should be output: 
                        ''' + '''
                        {
                        "available_times": null,
                        "next_button": "BOOK A TABLE"
                        }
                        ''' + f'''
                        {
                        """
                            These buttons have been tried and are NOT the 
                            correct next_button, do not return them as an answer: 
                        """ + str(incorrect_button_labels) if incorrect_button_labels else ""}
                        '''
                },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{encoded_image}" 
                        }
            ]
        
        prompt_dispatch = {
            "image_1": image_1
        }

        if prompt_type not in prompt_dispatch:
            raise ValueError(f"Prompt type {prompt_type} not found.")

        else:
            content_func = prompt_dispatch[prompt_type]
            content = content_func()
            return content