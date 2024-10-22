

class EvaluateConvenience:

    @staticmethod
    def evaluate(probability, environmentDescription, language):

        environmentImportance = EvaluateConvenience.getAiResponse(environmentDescription, language)

        # Define thresholds
        thresholds = {
            "very_critical": [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0],  # 10 levels
            "critical": [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 7.0, 12.0],
            "moderate": [0.1, 0.5, 1.0, 2.0, 5.0, 7.0, 10.0, 15.0, 20.0],
            "less_critical": [1.0, 3.0, 4.0, 5.0, 8.0, 10.0, 15.0, 25.0, 38.0, 42.0],
            "non_critical": [3.0, 4.0, 6.0, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0],
        }

        # Determine which set of thresholds to use based on environmental importance
        if environmentImportance > 0.8:  # Very critical
            threshold_set = thresholds["very_critical"]
        elif environmentImportance > 0.6:  # Critical
            threshold_set = thresholds["critical"]
        elif environmentImportance > 0.4:  # Moderate
            threshold_set = thresholds["moderate"]
        elif environmentImportance > 0.2:  # Less critical
            threshold_set = thresholds["less_critical"]
        else:  # Non-critical
            threshold_set = thresholds["non_critical"]


        if probability < threshold_set[0]:
            score = 10
        elif probability < threshold_set[1]:
            score = 9
        elif probability < threshold_set[2]:
            score = 8
        elif probability < threshold_set[3]:
            score = 7
        elif probability < threshold_set[4]:
            score = 6
        elif probability < threshold_set[5]:
            score = 4
        elif probability < threshold_set[6]:
            score = 3
        elif probability < threshold_set[7]:
            score = 2
        else:
            score = 1

        return score



    @staticmethod
    def getAiResponse(environmentDescription: str, language: bool):

        from openai import OpenAI
        import time

        API_KEY = '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'

        englishPrompt = """ 
        I am working on a system that models the performance of network environments using the concept of Packet Switching. 
        The higher the probability of many users being active at once, the more network congestion there is likely to be.
        In environments where network stability is critical (such as a university), 
        a high probability of simultaneous user activity is **not good** because it could cause delays or slowdowns in important tasks like accessing educational resources or completing academic work.
        Conversely, in environments where immediate access to the network is less critical (such as a café), 
        the system may tolerate higher user activity because people may be using the network more casually, 
        like for entertainment or casual browsing.  
        Even if there is a delay in packet switching, it would not have a serious impact on most users. 
        Considering that 0 is not important and 1 is very important. 
        Return me a number between 0 to 1 with a precision past the decimal point of 2, which indicates on how important is for people in an environment to not be disturbed by delaying internet.  
        Please respond with **only a number between 0 and 1**, representing the suitability of proceeding in the given environment. 
        The environment is:  """

        albanianPrompt = """ I am giving the environment in Albanian: """


        fullPrompt = ""
        if language: #english
          fullPrompt = f"{englishPrompt}{environmentDescription}"
        else:
          fullPrompt = f"{englishPrompt}{albanianPrompt}{environmentDescription}"

        print()
        print("Full Promt: ", fullPrompt)
        print()

        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=API_KEY
        )

        try:
            print("Making API call...")  # Indicate the start of the API call
            start_time = time.time()  # Track the start time


            # API call to get the completion
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[{"role": "user", "content": fullPrompt}],
                temperature=0.1,  # Lower temperature for more deterministic responses
                top_p = 1,
                max_tokens = 5,  # Small max_tokens as we're expecting a single number
                stream = False
            )

            elapsed_time = time.time() - start_time  # Calculate time taken for the request
            print(f"API call completed in {elapsed_time:.2f} seconds.")  # Show elapsed time

            # Extract the response content and strip any extra spaces
            print("_______________________")
            print("Result from AI: ",completion.choices[0].message.content)




            response_text = completion.choices[0].message.content

            response_text = response_text.replace("*", "")

            try:
                score = float(response_text)
                if 0 <= score <= 1:
                    return score
                else:
                    print(f"Received invalid score: {score}")
                    return -1  # Fallback in case of an invalid score
            except ValueError:
                print(f"Could not convert response to a float: {response_text}")
                return -1  # Fallback if the AI gives an unexpected response

        except Exception as e:
            print(f"An error occurred: {e}")
            return -1




#
# calculated_probability = 0.35
# environment_description = "an average home"
#
# # Get the AI's evaluation score from 0 to 1
# value = EvaluateConvenience.getAiResponse(environment_description, True)
# print(f"Returned suitability score: {value}")

#
