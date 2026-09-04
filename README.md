# Instructions for setting up Claude for AI-Assisted Threat Research

**Resources:**

1. The 'Detection Engineering Series' folder should be uploaed to the Claude
   project files. This contains the strategic guidance to help Claude understand
   best practices and key concepts.
2. The 'Completed TRR Reports' folder holds a 'flattened' copy of all the
   published TRR reports. These should be uploaded to the Claude project files
   as references. (You can update the collection as needed by downloading all
   the reports from the online library and running the `flatten_trr.py` script).
3. The files `TRR-OUTLINE.md` and `TRR-STYLE-GUIDE.md` should also be uploaded
   to the project files. These give Claude information about how to write TRRs.
4. The file `TRR-Research-Prompt_v*.md` contains the project instructons. The
   contents of this file should be pasted into the project's instructions. This
   is the most important part, as it gives Claude instructions on how to do the
   research, and how interact with you.

**Important Notes:**

You should not accept everything Claude tells you at face value. You need to
validate everything and redirect him with questions or assertions as needed.
While the instructions specifically address not making assumptions, Claude is
suspectible -- just like a human being -- to drawing incorrect conclusions.

Claude **excels** in rapidly gathering and synthesizing information, saving you
days or weeks of time finding and digesting the best resources yourself. He's
also great at identifying related concepts or issues and suggesting possible
procedures you might not have considered. And he's great at writing test cases
you can run to validate your understanding of each procedure and ultimately
check your coverage for each procedure.

But don't make the mistake of letting Claude do all the thinking. Ultimately,
you're still the expert.
