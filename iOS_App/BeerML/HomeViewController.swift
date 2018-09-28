//
//  HomeViewController.swift
//  BeerML
//
//  Created by Cristina De León on 9/27/18.
//  Copyright © 2018 Lazaro Kawer. All rights reserved.
//

import UIKit

class HomeViewController: UIViewController {
    
    @IBOutlet weak var scanBeerBtn: UIButton!
    @IBOutlet weak var creditsBtn: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        scanBeerBtn.layer.cornerRadius = 10
        creditsBtn.layer.cornerRadius = 10
    }
    
    @IBAction func scanButtonTapped(_ sender: Any) {
    }
    
    @IBAction func creditsButtonTapped(_ sender: Any) {
    }
    
}
