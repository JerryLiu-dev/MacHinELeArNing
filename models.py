import nn
import numpy as np
class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w,x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        if nn.as_scalar(self.run(x)) >= 0:
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        err = True
        errors = 0
        while err:
            errors = 0
            for x,y in dataset.iterate_once(1):
                if self.get_prediction(x) != nn.as_scalar(y):
                    errors +=1
                    self.w.update(x,nn.as_scalar(y))
            if errors == 0:
                err = False
        

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 200
        self.layer1 = nn.Parameter(1,512)
        self.layer2 = nn.Parameter(512,1)
        self.bias1 = nn.Parameter(1,512)
        self.bias2 = nn.Parameter(1,1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        hidden = nn.Linear(x,self.layer1)
        hidden = nn.AddBias(hidden,self.bias1)
        hidden = nn.ReLU(hidden)
        output = nn.Linear(hidden,self.layer2)
        output == nn.AddBias(output,self.bias2)
    
        return output

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        
        loss = nn.SquareLoss(self.run(x),y)
        return loss

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        lRate = -0.05
        loss = 0
        count = 0
        while True:
            for x,y in dataset.iterate_once(self.batch_size):
                temp_loss = self.get_loss(x,y)
                grad_wrt_l1, grad_wrt_l2, grad_wrt_b1,grad_wrt_b2 = nn.gradients(temp_loss, [self.layer1,self.layer2,self.bias1,self.bias2])
               
                self.layer1.update(grad_wrt_l1,lRate)
                self.layer2.update(grad_wrt_l2,lRate)
                self.bias1.update(grad_wrt_b1,lRate)
                self.bias2.update(grad_wrt_b2,lRate)
            loss += nn.as_scalar(temp_loss)
            count += 1
                
            if float(loss / count) < 0.02:
                return


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 100
        self.layer1 = nn.Parameter(784,200)
        self.layer2 = nn.Parameter(200,10)
        self.bias1 = nn.Parameter(1,200)
        self.bias2 = nn.Parameter(1,10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        hidden = nn.Linear(x,self.layer1)
        hidden = nn.AddBias(hidden,self.bias1)
        hidden = nn.ReLU(hidden)
        output = nn.Linear(hidden,self.layer2)
        output = nn.AddBias(output, self.bias2)
        return output
    
    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

        logits = self.run(x)
        return nn.SoftmaxLoss(logits, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        lRate = -0.5
        while True:
            for x,y in dataset.iterate_once(self.batch_size):
                temp_loss = self.get_loss(x,y)
                grad_wrt_l1, grad_wrt_l2, grad_wrt_b1,grad_wrt_b2 = nn.gradients(temp_loss, [self.layer1,self.layer2,self.bias1,self.bias2])
               
                self.layer1.update(grad_wrt_l1,lRate)
                self.layer2.update(grad_wrt_l2,lRate)
                self.bias1.update(grad_wrt_b1,lRate)
                self.bias2.update(grad_wrt_b2,lRate)
                
            if dataset.get_validation_accuracy() > .97:
                return
class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 75
        self.w_x = nn.Parameter(self.num_chars, 512) # input x initial weights
        self.w_h = nn.Parameter(512, 512) # hidden weights
        self.w_output = nn.Parameter(512, 5) # hidden x 5 for the 5 languages
        self.bias_x = nn.Parameter(1, 512)
        # self.bias_h = nn.Parameter(1, 512)
        # self.bias_o = nn.Parameter(1, 5)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h = nn.Linear(xs[0], self.w_x)
        for _, x in enumerate(xs[1:]):
            x_Wx = nn.Linear(x, self.w_x)
            x_Wx = nn.AddBias(x_Wx, self.bias_x)
            # x_Wx = nn.ReLU(x_Wx)
            h_Wh = nn.Linear(h, self.w_h)
            # h_Wh = nn.AddBias(h_Wh, self.bias_h)

            h = nn.Add(x_Wx, h_Wh)
            h = nn.ReLU(h)

        output = nn.Linear(h, self.w_output)
        # output = nn.AddBias(output, self.bias_o)
        return output

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        logits = self.run(xs)
        return nn.SoftmaxLoss(logits, y)
    
    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        lRate = -0.1
        while True:
            for x,y in dataset.iterate_once(self.batch_size):
                temp_loss = self.get_loss(x,y)
                grad_wrt_wx, grad_wrt_wh, grad_wrt_wo, grad_wrt_bias_x = nn.gradients(temp_loss, [self.w_x, self.w_h, self.w_output,self.bias_x])
               
                self.w_x.update(grad_wrt_wx,lRate)
                self.w_h.update(grad_wrt_wh,lRate)
                self.w_output.update(grad_wrt_wo,lRate)
                self.bias_x.update(grad_wrt_bias_x,lRate)
                # self.bias_h.update(grad_wrt_bias_h,lRate)
                # self.bias_o.update(grad_wrt_bias_o,lRate)
                
            if dataset.get_validation_accuracy() > .89:
                return
