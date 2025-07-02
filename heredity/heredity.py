import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        # Trait is None 
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    # Hints
    '''
    Note 1:
        parents not listed: use unconditional probabilities.
        parents listed: compute based on parents' gene counts and mutation (conditional probabilities).
    Note 02:
        Trait is True => scenario enumeration: Only True cases => joint probability: must have Trait
        Trait is False => scenario enumeration: Only False cases => joint probability: must not have Trait
        Trait is None => exclude in fails_evidence loop of main()
    '''
    
    joint_prob = 1 # starting value to be multiplied later
    parents_listed = {person for person in people if people[person]["mother"] and people[person]["father"]}

    for person in people:
        shown_trait = person in have_trait # boolean object => None value is passed in fails_evidence
        copies_of_gene = 1 if person in one_gene else 2 if person in two_genes else 0

        # uncondional probabilities
        if person not in parents_listed: 
            prob = PROBS["gene"][copies_of_gene] * PROBS["trait"][copies_of_gene][shown_trait]
            joint_prob *= prob

        # conditional on parents' gene and mutation = they are the children
        else:
            # Probability that a parent passes mutated 1 copy of mutated gene to the child
            def pass_mutated_gene_to_child(parent):
                if parent in two_genes: # almost always pass 1 copy of mutated gene,if there is no mutation
                    return 1 - PROBS["mutation"] # no mutation probability
                elif parent in one_gene: # only 1 in 2 copies of gene (50% randomness) is mutated and will be passed to the child
                    return 0.5 # prob of mutation only applies in 0 or 2 copies of mutated gene => read UNDERSTANDING
                else: # 0 copy of gene is mutated => always pass healthy gene unless mutation occurs
                    return PROBS["mutation"] # probability of mutation

            pass_mother = pass_mutated_gene_to_child(people[person]["mother"])
            pass_father = pass_mutated_gene_to_child(people[person]["father"])

            # Probability child gets copies_of_gene: every child get 1 copy from both mother and father
            '''
            0 copies of gene: both parents passed no mutated gene
            1 copies of gene: either mother XOR father passed a mutated gene
            2 copies of gene: both parent passed mutated gene (each parent passed 1 copy of gene to the child)
            '''

            prob_child = 1 # starting value to be multiplied later
            if copies_of_gene == 0:
                prob_child = (1 - pass_mother) * (1 - pass_father)
            elif copies_of_gene == 1:
                prob_child = pass_mother * (1 - pass_father) + (1 - pass_mother) * pass_father
            else:
                prob_child = pass_mother * pass_father
            
            joint_prob *= (prob_child * PROBS["trait"][copies_of_gene][shown_trait])

    # multiply all elements of the list
    return joint_prob



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        copies_of_gene = 1 if person in one_gene else 2 if person in two_genes else 0
        probabilities[person]["gene"][copies_of_gene] += p
        probabilities[person]["trait"][person in have_trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """ 

    for person in probabilities:
        for field in ["gene", "trait"]:
            unnormalized_sum = sum(probabilities[person][field].values())
            if unnormalized_sum == 0: # avoid Zero Division Error
                continue
            for key in probabilities[person][field]:
                probabilities[person][field][key] /= unnormalized_sum

    '''
    def cal(arg):
        unnormalized_sum = sum(arg[i] for i in arg)
        for i in arg:
            arg[i] /= unnormalized_sum

    for person in probabilities:
        cal(probabilities[person]["gene"])
        cal(probabilities[person]["trait"])
    '''    

        
if __name__ == "__main__":
    main()
